# Folder Synchronization Tool

## Overview

This Python script synchronizes two folders. It ensures that a source folder and a replica folder are kept in sync. The script uses the `watchdog` library to monitor changes in the source folder and updates the replica folder accordingly. 

## Features

- **Initial Synchronization**: Copies files from the source to the replica folder and updates files that have changed.
- **Real-Time Monitoring**: Uses `watchdog` to monitor the source folder for changes and synchronizes these changes to the replica folder.
- **Logging**: Logs synchronization events to a log file.


## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/EuricoSantos-936/Folder-Sync-Python.git
   ```

2. **Navigate to the Project Directory**

```bash
cd Folder-Sync-Python
```

3. **Create and Activate a Virtual Environment** (Not required)

```bash
python3 -m venv env
source env/bin/activate
```

4. **Install Dependencies**

```bash
pip install -r requirements.txt
```

## Usage

1. **Run the Script**

```bash
python3 app.py /path/to/source_folder   
```
    - Replace /path/to/source_folder with the path to the folder you want to synchronize. The script will create a replica folder at the same level as the source folder, named <source_folder>_sync, and log synchronization events to sync.log.

2. **View Log File**

The log file sync.log will be created in the same directory as the source folder. It records the following events:

    .File Created: When a new file is copied from the source to the replica.
    .File Updated: When a file in the replica is updated to match the source.
    .File Deleted: When a file is deleted from the replica.
    .Directory Created/Deleted: When directories are created or deleted.

## Contribution

If you would like to contribute to this project, please fork the repository and submit a pull request. Ensure that your changes are well-documented and include tests where appropriate.

## Acknowledgments

- **Watchdog**: For real-time file system monitoring.
- **Python**: For being a versatile programming language.

For any questions or issues, please contact euricosantos_936@hotmail.com or open an issue on the GitHub repository.

### Explanation

1. **Overview**: Describes what the script does.
2. **Features**: Lists the key features of the tool.
3. **Requirements**: Lists the necessary software and libraries.
4. **Installation**: Provides step-by-step instructions to set up the project.
5. **Usage**: Explains how to run the script and what the log file contains.
6. **Contributing**: Instructions for contributing to the project.
7. **License**: Licensing information.
8. **Acknowledgments**: Credits to tools and libraries used.