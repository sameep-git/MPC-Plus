#!/usr/bin/env python3
"""
iDrive Folder Monitor - Entry Point for MPC-Plus Data Processing

This program monitors the 'iDrive' folder for new directory uploads and 
automatically processes them using the DataProcessor.

Author: MPC-Plus System
"""

import os
import sys
import time
import logging
from pathlib import Path
from dotenv import load_dotenv

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from src.data_manipulation.ETL.DataProcessor import DataProcessor

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/folder_monitor.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class iDriveFolderHandler(FileSystemEventHandler):
    """
    Event handler for monitoring iDrive folder changes
    """
    
    def __init__(self, supabase_url=None, supabase_key=None):
        """
        Initialize the handler
        
        Args:
            supabase_url (str, optional): Supabase URL for uploads
            supabase_key (str, optional): Supabase API key for uploads
        """
        self.processed_folders = set()  # Track processed folders to avoid duplicates
        self.supabase_url = supabase_url
        self.supabase_key = supabase_key
        
    def on_created(self, event):
        """
        Handle file/folder creation events
        
        Args:
            event: FileSystemEvent object
        """
        if event.is_directory:
            self._process_new_folder(event.src_path)
    
    def on_moved(self, event):
        """
        Handle file/folder move events (covers uploads that appear as moves)
        
        Args:
            event: FileSystemEvent object
        """
        if event.is_directory:
            self._process_new_folder(event.dest_path)
    
    def _process_new_folder(self, folder_path):
        """
        Process a newly detected folder
        
        Args:
            folder_path (str): Path to the newly created/moved folder
        """
        try:
            # Avoid processing the same folder multiple times
            if folder_path in self.processed_folders:
                return
                
            logger.info(f"New folder detected: {folder_path}")
            
            # Add a small delay to ensure the upload is complete
            time.sleep(2)
            
            # Verify the folder still exists and contains files
            if not self._is_folder_ready(folder_path):
                logger.warning(f"Folder not ready or incomplete: {folder_path}")
                return
            
            # Mark as processed to avoid duplicates
            self.processed_folders.add(folder_path)
            
            # Create DataProcessor instance and run processing
            logger.info(f"Processing folder: {folder_path}")
            processor = DataProcessor(
                folder_path, 
                supabase_url=self.supabase_url,
                supabase_key=self.supabase_key
            )
            processor.Run()
            
            logger.info(f"Successfully processed folder: {folder_path}")
            
        except Exception as e:
            logger.error(f"Error processing folder {folder_path}: {str(e)}")
            # Remove from processed set so we can retry later if needed
            self.processed_folders.discard(folder_path)
    
    def _is_folder_ready(self, folder_path):
        """
        Check if a folder is ready for processing (contains expected files)
        
        Args:
            folder_path (str): Path to check
            
        Returns:
            bool: True if folder is ready for processing
        """
        try:
            if not os.path.exists(folder_path):
                return False
                
            # Check if Results.csv exists (required by DataProcessor)
            results_csv = os.path.join(folder_path, "Results.csv")
            if not os.path.exists(results_csv):
                logger.debug(f"Results.csv not found in {folder_path}, waiting...")
                return False
            
            # Check if file is not empty and not being written to
            if os.path.getsize(results_csv) == 0:
                return False
                
            return True
            
        except Exception as e:
            logger.error(f"Error checking folder readiness {folder_path}: {str(e)}")
            return False

class FolderMonitor:
    """
    Main folder monitoring service
    """
    
    def __init__(self, idrive_path="iDrive", supabase_url=None, supabase_key=None):
        """
        Initialize the folder monitor
        
        Args:
            idrive_path (str): Path to the iDrive folder to monitor
            supabase_url (str, optional): Supabase URL for uploads
            supabase_key (str, optional): Supabase API key for uploads
        """
        self.idrive_path = os.path.abspath(idrive_path)
        self.observer = Observer()
        self.handler = iDriveFolderHandler(supabase_url, supabase_key)
        self.is_running = False
        
    def start_monitoring(self):
        """
        Start monitoring the iDrive folder
        """
        try:
            # Ensure iDrive folder exists
            if not os.path.exists(self.idrive_path):
                logger.warning(f"iDrive folder does not exist: {self.idrive_path}")
                logger.info(f"Creating iDrive folder: {self.idrive_path}")
                os.makedirs(self.idrive_path, exist_ok=True)
            
            logger.info(f"Starting folder monitoring on: {self.idrive_path}")
            
            # Set up observer
            self.observer.schedule(self.handler, self.idrive_path, recursive=True)
            self.observer.start()
            self.is_running = True
            
            logger.info("Folder monitoring started successfully")
            logger.info("Press Ctrl+C to stop monitoring")
            
            # Keep the program running
            try:
                while self.is_running:
                    time.sleep(1)
            except KeyboardInterrupt:
                logger.info("Received interrupt signal, stopping...")
                self.stop_monitoring()
                
        except Exception as e:
            logger.error(f"Error starting folder monitoring: {str(e)}")
            sys.exit(1)
    
    def stop_monitoring(self):
        """
        Stop monitoring the folder
        """
        if self.is_running:
            logger.info("Stopping folder monitoring...")
            self.observer.stop()
            self.observer.join()
            self.is_running = False
            logger.info("Folder monitoring stopped")
    
    def scan_existing_folders(self):
        """
        Scan for existing folders that might need processing
        """
        try:
            logger.info("Scanning for existing folders in iDrive...")
            
            if not os.path.exists(self.idrive_path):
                logger.info("iDrive folder does not exist yet")
                return
            
            for item in os.listdir(self.idrive_path):
                item_path = os.path.join(self.idrive_path, item)
                if os.path.isdir(item_path):
                    logger.info(f"Found existing folder: {item_path}")
                    # Process existing folder if it hasn't been processed
                    self.handler._process_new_folder(item_path)
                    
        except Exception as e:
            logger.error(f"Error scanning existing folders: {str(e)}")

def main():
    """
    Main entry point for the folder monitor
    """
    logger.info("=== MPC-Plus iDrive Folder Monitor Starting ===")
    
    # Load Supabase credentials from environment variables (if available)
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    
    if supabase_url and supabase_key:
        logger.info("✓ Supabase credentials loaded - uploads will be enabled")
    else:
        logger.info("⚠ No Supabase credentials found - uploads will be disabled")
        logger.info("  Set SUPABASE_URL and SUPABASE_KEY in .env file to enable uploads")
    
    # Create and configure monitor
    monitor = FolderMonitor(
        supabase_url=supabase_url,
        supabase_key=supabase_key
    )
    
    # Scan for existing folders first
    #monitor.scan_existing_folders()
    
    # Start continuous monitoring
    monitor.start_monitoring()

if __name__ == "__main__":
    main()
