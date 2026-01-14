#!/usr/bin/env python3
"""
Script to ingest all missed 2.5x beam data from the Lexar drive.
This script finds all BeamCheckTemplate2.5x folders and processes them.
"""

import os
import sys
import logging
from pathlib import Path

# Add project root to path to import DataProcessor
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.data_manipulation.ETL.DataProcessor import DataProcessor

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('2.5x_ingestion.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def find_2_5x_folders(base_path):
    """
    Find all folders containing BeamCheckTemplate2.5x in the given path.
    
    Args:
        base_path: Base directory to search
        
    Returns:
        List of folder paths
    """
    folders = []
    if not os.path.exists(base_path):
        logger.error(f"Base path does not exist: {base_path}")
        return folders
    
    for root, dirs, files in os.walk(base_path):
        for dir_name in dirs:
            if "BeamCheckTemplate2.5x" in dir_name:
                folder_path = os.path.join(root, dir_name)
                # Verify Results.csv exists
                results_csv = os.path.join(folder_path, "Results.csv")
                if os.path.exists(results_csv):
                    folders.append(folder_path)
                    logger.info(f"Found 2.5x beam folder: {folder_path}")
                else:
                    logger.warning(f"Found 2.5x folder but Results.csv missing: {folder_path}")
    
    return folders

def process_folder(folder_path):
    """
    Process a single 2.5x beam folder.
    
    Args:
        folder_path: Path to the beam folder
        
    Returns:
        True if successful, False otherwise
    """
    try:
        logger.info(f"Processing folder: {folder_path}")
        processor = DataProcessor(folder_path)
        processor.Run()
        logger.info(f"Successfully processed: {folder_path}")
        return True
    except Exception as e:
        logger.error(f"Error processing {folder_path}: {str(e)}", exc_info=True)
        return False

def main():
    """Main function to find and process all 2.5x beam folders."""
    # Path to Lexar drive
    lexar_path = "/Volumes/Lexar/MPC Data/Arlington"
    
    logger.info(f"Searching for 2.5x beam folders in: {lexar_path}")
    
    # Find all 2.5x folders
    folders = find_2_5x_folders(lexar_path)
    
    if not folders:
        logger.warning("No 2.5x beam folders found!")
        return
    
    logger.info(f"Found {len(folders)} 2.5x beam folders to process")
    
    # Process each folder
    success_count = 0
    failure_count = 0
    
    for i, folder_path in enumerate(folders, 1):
        logger.info(f"Processing {i}/{len(folders)}: {folder_path}")
        if process_folder(folder_path):
            success_count += 1
        else:
            failure_count += 1
    
    # Summary
    logger.info("=" * 60)
    logger.info("INGESTION SUMMARY")
    logger.info("=" * 60)
    logger.info(f"Total folders found: {len(folders)}")
    logger.info(f"Successfully processed: {success_count}")
    logger.info(f"Failed: {failure_count}")
    logger.info("=" * 60)

if __name__ == "__main__":
    main()

