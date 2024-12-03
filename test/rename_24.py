import os

def rename_folders(directory):
    # Iterate over all subfolders in the given directory
    subdirs = os.listdir(directory)
    # print (subdirs)
    for folder_name in subdirs:
        # Check if the folder name follows the naming convention and ends with '_24'
        if folder_name.count('_') == 2 and folder_name.startswith('24_'):
            parts = folder_name.split('_')
            # print(parts)
            if len(parts[0]) == 2 and parts[0] == '24':
                # Swap the first two digits with the last two digits
                parts[0] = '2024'
                new_name = f"{parts[0]}_{parts[1]}_{parts[2]}"
                # Get the full path for renaming
                old_path = os.path.join(directory, folder_name)
                new_path = os.path.join(directory, new_name)
                # Rename the folder
                os.rename(old_path, new_path)
                print(f"Renamed: {folder_name} -> {new_name}")

if __name__ == "__main__":
    # Replace 'your_directory_path' with the path to the folder containing the subfolders
    directory_path = "/blueprod/STOR2/stor2/kshetra/forClient/mantapa_v02/mail"
    rename_folders(directory_path)
