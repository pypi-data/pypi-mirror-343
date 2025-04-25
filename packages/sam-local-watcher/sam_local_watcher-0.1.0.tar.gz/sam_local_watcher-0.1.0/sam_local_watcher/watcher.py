"""
Core functionality for SAM Local Watcher.

This module provides the main functionality for watching file changes in a SAM project
and syncing them to the .aws-sam/build directory.
"""

import time
import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from cfn_tools import load_yaml
import yaml


class FileChangeHandler(FileSystemEventHandler):
    """
    Handler for file system events to sync changes to SAM build directory.
    """
    
    def __init__(self, function_mapping, folder_to_watch):
        """
        Initialize the file change handler.
        
        Args:
            function_mapping (dict): Mapping of source directories to function names
            folder_to_watch (str): Base folder being watched
        """
        self.function_mapping = function_mapping
        self.folder_to_watch = folder_to_watch
    
    def on_created(self, event):
        """Handle file creation events."""
        if not event.is_directory:
            print(f"File created: {event.src_path}")
    
    def on_modified(self, event):
        """
        Handle file modification events and sync changes to build directory.
        
        Only syncs files with extensions: txt, py, js, json
        """
        if not event.is_directory and any(event.src_path.endswith(ext) for ext in ['txt', 'py', 'js', 'json']):
            for prefix in self.function_mapping:
                if event.src_path.startswith(prefix):
                    filename = event.src_path[len(prefix):]
                    for function in self.function_mapping[prefix]:
                        cpy1 = f"{event.src_path}"
                        cpy2 = f"{self.folder_to_watch}/.aws-sam/build/{function}/{filename}"
                        shutil.copy2(cpy1, cpy2)
                        print(f"copying... {cpy1[len(self.folder_to_watch)+1:]} to {cpy2[len(self.folder_to_watch)+1:]}")
    
    def on_deleted(self, event):
        """Handle file deletion events."""
        if not event.is_directory:
            print(f"File deleted: {event.src_path}")
    
    def on_moved(self, event):
        """Handle file move events."""
        if not event.is_directory:
            print(f"File moved from {event.src_path} to {event.dest_path}")


def find_serverless_functions(file_path):
    """
    Find all AWS::Serverless::Function resources in a SAM template YAML file.
    
    Args:
        file_path (str): Path to the YAML file
        
    Returns:
        dict: Dictionary of function resources found
    """
    try:
        with open(file_path, 'r') as yaml_file:
            yaml_content = load_yaml(yaml_file)
            
            if not yaml_content or 'Resources' not in yaml_content:
                print("No Resources section found in the YAML file.")
                return {}
            
            # Find all resources with Type: AWS::Serverless::Function
            serverless_functions = {}
            for resource_name, resource_details in yaml_content['Resources'].items():
                if resource_details.get('Type') == 'AWS::Serverless::Function':
                    serverless_functions[resource_name] = resource_details
            
            return serverless_functions
            
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return {}
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        return {}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {}


def watch_folder(path, yaml_path="template.yaml"):
    """
    Watch a folder for changes and sync them to the SAM build directory.
    
    Args:
        path (str): Path to the folder to watch
        yaml_path (str, optional): Path to the SAM template YAML file. Defaults to "template.yaml".
    """
    folder_to_watch = os.path.abspath(path)
    
    # Find all serverless functions
    serverless_functions = find_serverless_functions(yaml_path)
    
    # Create function mapping
    function_mapping = {}
    for function in serverless_functions:
        path_prefix = folder_to_watch + '/' + serverless_functions[function]['Properties']['CodeUri']
        
        if path_prefix not in function_mapping:
            function_mapping[path_prefix] = []
            
        function_mapping[path_prefix].append(function)
    
    # Set up the observer
    event_handler = FileChangeHandler(function_mapping, folder_to_watch)
    observer = Observer()
    observer.schedule(event_handler, folder_to_watch, recursive=True)
    observer.start()
    
    try:
        print(f"Watching for file changes in {folder_to_watch} and its subfolders...")
        print("Press Ctrl+C to stop")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
