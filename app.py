import argparse
import logging
import os
import hashlib
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def calculate_hash(file_path):
    """
    Calculate the MD5 hash of a file.

    :param str file_path: Path to the file
    :return: The MD5 hash of the file
    :rtype: str
    """
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)

    return hash_md5.hexdigest()

def sync_folders(source_folder, replica_folder, log_file):
    """
    Synchronize the contents of the source folder to the replica folder.

    :param str source_folder: Path to the source folder
    :param str replica_folder: Path to the replica folder
    :param str log_file: Path to the log file
    """
    if not os.path.exists(replica_folder):
        os.makedirs(replica_folder)
        logging.info(f"Directory created: {replica_folder}")

    source_files = {}
    for dirpath, dirnames, filenames in os.walk(source_folder):
        replica_dirpath = dirpath.replace(source_folder, replica_folder, 1)

        if not os.path.exists(replica_dirpath):
            os.makedirs(replica_dirpath)
            logging.info(f"Directory created: {replica_dirpath}")

        for filename in filenames:
            if filename == os.path.basename(log_file):
                continue
            source_file = os.path.join(dirpath, filename)
            replica_file = os.path.join(replica_dirpath, filename)
            source_files[replica_file] = source_file

            if not os.path.exists(replica_file):
                shutil.copy2(source_file, replica_file)
                logging.info(f"File copied: {replica_file}")
            else:
                if calculate_hash(source_file) != calculate_hash(replica_file):
                    shutil.copy2(source_file, replica_file)
                    logging.info(f"File updated: {replica_file}")

    # Check for missing files in the replica folder and restore them
    for dirpath, dirnames, filenames in os.walk(source_folder):
        replica_dirpath = dirpath.replace(source_folder, replica_folder, 1)
        
        if not os.path.exists(replica_dirpath):
            os.makedirs(replica_dirpath)
            logging.info(f"Directory created: {replica_dirpath}")

        for filename in filenames:
            source_file = os.path.join(dirpath, filename)
            replica_file = os.path.join(replica_dirpath, filename)

            if not os.path.exists(replica_file):
                shutil.copy2(source_file, replica_file)
                logging.info(f"File restored: {replica_file}")

    # Remove files in the replica folder that are no longer in the source folder
    for dirpath, dirnames, filenames in os.walk(replica_folder, topdown=False):
        for filename in filenames:
            replica_file = os.path.join(dirpath, filename)
            if replica_file not in source_files:
                if os.path.exists(replica_file):
                    os.remove(replica_file)
                    logging.info(f"File deleted: {replica_file}")

        for dirname in dirnames:
            replica_dirpath = os.path.join(dirpath, dirname)
            source_dir = replica_dirpath.replace(replica_folder, source_folder, 1)
            if not os.path.exists(source_dir):
                shutil.rmtree(replica_dirpath)
                logging.info(f"Directory deleted: {replica_dirpath}")

def setup_logging(log_path):
    """
    Set up logging configuration.

    Ensures that the log directory exists and configures the
    logging module to log at the INFO level to the specified
    log file, appending to the file if it already exists.

    :param str log_path: The path to the log file.
    """

    log_dir = os.path.dirname(log_path)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Set up logging configuration
    logging.basicConfig(
        level=logging.INFO,
        filename=log_path,
        format='%(asctime)s - %(message)s',
        filemode='a' 
    )

class SyncHandler(FileSystemEventHandler):
    """
    Handles file system events and triggers synchronization.
    """
    def __init__(self, source_folder, replica_folder, log_file):
        self.source_folder = source_folder
        self.replica_folder = replica_folder
        self.log_file = log_file

    def on_any_event(self, event):
        sync_folders(self.source_folder, self.replica_folder, self.log_file)

def main():
    """
    Entry point for the script.

    Syncs the source folder with a replica folder and sets up an event handler to monitor
    for changes to the source folder. The replica folder is created if it does not exist.
    And have a log file to check folder updates.
    The script takes a single command line argument: the path to the source folder.
    """

    parser = argparse.ArgumentParser(description="Sync two folders")
    parser.add_argument('source_folder', type=str, help="Source folder")
    args = parser.parse_args()

    source_folder = args.source_folder
    replica_folder = os.path.join(os.path.dirname(source_folder), os.path.basename(source_folder) + '_sync')
    
    # Define the log file path at the same level as source and replica folders
    log_file_path = os.path.join(os.path.dirname(source_folder), 'sync.log')

    if not os.path.exists(source_folder):
        print(f"Source folder does not exist: {source_folder}")
        return

    # Setup logging
    setup_logging(log_file_path)

    # Synchronize initially, even if the replica folder exists
    sync_folders(source_folder, replica_folder, log_file_path)

    # Set up the event handler to monitor for changes
    event_handler = SyncHandler(source_folder, replica_folder, log_file_path)
    observer = Observer()
    observer.schedule(event_handler, path=source_folder, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(30)
            sync_folders(source_folder, replica_folder, log_file_path)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

if __name__ == '__main__':
    main()
