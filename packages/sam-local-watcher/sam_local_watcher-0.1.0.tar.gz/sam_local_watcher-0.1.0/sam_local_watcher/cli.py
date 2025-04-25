"""
Command-line interface for SAM Local Watcher.
"""

import argparse
import os
from .watcher import watch_folder


def main():
    """
    Main entry point for the command-line interface.
    """
    parser = argparse.ArgumentParser(
        description='Watch and sync files for AWS SAM local development'
    )
    
    parser.add_argument(
        '-p', '--path',
        default='.',
        help='Path to the SAM project directory (default: current directory)'
    )
    
    parser.add_argument(
        '-t', '--template',
        default='template.yaml',
        help='Path to the SAM template file (default: template.yaml)'
    )
    
    args = parser.parse_args()
    
    # Convert to absolute path if relative
    path = os.path.abspath(args.path)
    template_path = os.path.join(path, args.template)
    
    # Start watching
    watch_folder(path, template_path)


if __name__ == '__main__':
    main()
