#!/usr/bin/env python3
"""
MPC-Plus Main Entry Point

This is the main entry point for the MPC-Plus system. It provides a simple
command-line interface to start the folder monitoring service and other
system components.
"""

import os
import sys
import argparse
import logging
from pathlib import Path

# Add the project root to the Python path
# This file is at: MPC-Plus/src/data_manipulation/file_monitoring/main.py
# We want to add: MPC-Plus/ to the path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.data_manipulation.file_monitoring.folder_monitor import FolderMonitor
from src.data_manipulation.file_monitoring.run_monitor_service import MonitorService, install_dependencies

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def print_banner():
    """Print the MPC-Plus banner"""
    print("=" * 50)
    print("    MPC-Plus - Medical Physics Console Plus")
    print("    Automated Data Processing System")
    print("=" * 50)
    print()

def start_monitor(idrive_path="iDrive", background=False):
    """
    Start the folder monitor
    
    Args:
        idrive_path (str): Path to monitor
        background (bool): Whether to run in background
    """
    try:
        print(f"Starting folder monitor for: {os.path.abspath(idrive_path)}")
        
        if background:
            # Use the service runner for background mode
            service = MonitorService()
            service.start_background()
        else:
            # Direct monitoring mode
            monitor = FolderMonitor(idrive_path)
            monitor.scan_existing_folders()
            monitor.start_monitoring()
            
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        logger.error(f"Error starting monitor: {str(e)}")
        sys.exit(1)

def setup_system():
    """
    Set up the MPC-Plus system
    """
    print("Setting up MPC-Plus system...")
    
    # Install dependencies
    if not install_dependencies():
        print("ERROR: Failed to install dependencies")
        return False
    
    # Create default iDrive folder if it doesn't exist
    idrive_path = "iDrive"
    if not os.path.exists(idrive_path):
        print(f"Creating iDrive folder: {os.path.abspath(idrive_path)}")
        os.makedirs(idrive_path, exist_ok=True)
    
    # Create logs directory
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        print(f"Creating logs directory: {os.path.abspath(logs_dir)}")
        os.makedirs(logs_dir, exist_ok=True)
    
    print("System setup completed successfully!")
    print()
    print("You can now start the monitor with:")
    print("  python src/main.py start")
    return True

def main():
    """
    Main entry point
    """
    parser = argparse.ArgumentParser(
        description='MPC-Plus - Medical Physics Console Plus',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python src/main.py setup           # Set up the system
  python src/main.py start           # Start folder monitoring
  python src/main.py start --path custom_folder  # Monitor custom folder
  python src/main.py start --background          # Run in background
  python -m src.data_manipulation.file_monitoring.main start
        """
    )
    
    parser.add_argument('command', choices=['setup', 'start', 'status'], 
                       help='Command to execute')
    parser.add_argument('--path', '-p', default='iDrive',
                       help='Path to monitor (default: iDrive)')
    parser.add_argument('--background', '-b', action='store_true',
                       help='Run in background mode')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose logging')
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    print_banner()
    
    if args.command == 'setup':
        setup_system()
    elif args.command == 'start':
        start_monitor(args.path, args.background)
    elif args.command == 'status':
        service = MonitorService()
        service.status()

if __name__ == "__main__":
    main()
