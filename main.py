import os
import shutil
import sys
import json
import argparse

user_home = os.path.expanduser("~")

class FileOrganizer:
    def __init__(self, folder, verbose=False, dry_run=False):
        self.directory = os.path.join(os.path.expanduser("~"), folder)
        self.verbose = verbose
        self.dry_run = dry_run
        
        config_dir = os.path.dirname(os.path.abspath(__file__))
        os.makedirs(config_dir, exist_ok=True)
        
        self.config_path = os.path.join(config_dir, "config.json")
        print("Config path:", self.config_path)
        
        self.load_config()
        
    def log(self, message):
        if self.verbose:
            print(message)
        
    def init(self):
        try:
            files = os.listdir(self.directory)
        except FileNotFoundError:
            print(f"The directory '{self.directory}' could not be found.")
            return
        except PermissionError:
            print(f"Permission denied to access '{self.directory}'.")
            return

        self.organize(files)


    def load_config(self):
            if not os.path.exists(self.config_path):
                self.create_default_config()
            try:
                with open(self.config_path, 'r') as file:
                    self.config = json.load(file)
                    
            except Exception as e:
                print(f"Failed to load configuration file: {e}")
                sys.exit(1)
                
    def create_default_config(self):
            default_config = {
                "extensions": {
                    ".jpg": "Images",
                    ".png": "Images",
                    ".gif": "Images",
                    ".mp4": "Videos",
                    ".doc": "Docs",
                    ".pdf": "Docs",
                    ".txt": "Docs",
                    ".blend": "Blender Models",
                    ".blend1": "Blender Models",
                    ".fbx": "FBX Exports",
                    ".mp3": "Music",
                    ".wav": "Music"
                    }
                }
            with open(self.config_path, 'w') as file:
                json.dump(default_config, file, indent=4)
            print(f"Default configuration file created at: {self.config_path}")

    @staticmethod
    def unique_path(path):
        base, ext = os.path.splitext(path)
        counter = 1
        while os.path.exists(path):
            path = f"{base} ({counter}){ext}"
            counter += 1
        return path
    
    
    def organize(self, files):
        extensions = self.config["extensions"]
        
        for filename in files:
            file_path = os.path.join(self.directory, filename)
            
            if not os.path.isfile(file_path):
                self.log(f"Skipped {filename}. It is a directory.")
                continue
                
            extension = os.path.splitext(filename)[1].lower()
            
            if extension not in extensions:
                self.log(f"Skipped {filename}. Unknown file extension.")
                continue
            
            folder_name = extensions[extension]
            folder_path = os.path.join(self.directory, folder_name)
            destination_path = self.unique_path(os.path.join(folder_path, filename))
            
            if self.dry_run:
                print(f"[dry run] Would move {filename} to {folder_name} folder.")
            else:
                os.makedirs(folder_path, exist_ok=True)
                shutil.move(file_path, destination_path)
                print(f"Moved {filename} to {folder_name} folder.")
            
            

def main():
    parser = argparse.ArgumentParser(description="Sort files in a folder by extension.")
    parser.add_argument("folder", help="Folder inside your home directory, e.g. Documents")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show skipped items")
    parser.add_argument("-n", "--dry-run", action="store_true", help="Show what would move without moving")
    args = parser.parse_args()
    
    organizer = FileOrganizer(args.folder, verbose=args.verbose, dry_run=args.dry_run)
    organizer.init()
            
if __name__ == '__main__':
    main()