import os
from datetime import datetime, timedelta

def is_folder_stale(folder_path, days=60):
    """
    Check the folder and all its contents recursively.
    Returns True if every file and subfolder (including the folder itself)
    has a modification time older than 'days' days.
    """
    threshold = timedelta(days=days)
    now = datetime.now()
    for root, dirs, files in os.walk(folder_path):
        # Check the current folder's modification time
        if now - datetime.fromtimestamp(os.path.getmtime(root)) < threshold:
            return False
        # Check each file's modification time in the current folder
        for file in files:
            file_path = os.path.join(root, file)
            if now - datetime.fromtimestamp(os.path.getmtime(file_path)) < threshold:
                return False
    return True

def check_folder_modification_time(root_folder, days=60):
    """
    Walk through each folder in 'root_folder' and print it only if
    all its items (files and subfolders) are older than 'days' days.
    """
    for dirpath, dirnames, filenames in os.walk(root_folder):
        # Check only if the folder and its content are stale
        if is_folder_stale(dirpath, days):
            print(f"Folder: {dirpath} is stale (all contents modified more than {days} days ago)")

# Example usage
folder_to_check = '/crap/versionCache'  # Replace with your folder path
check_folder_modification_time(folder_to_check)
