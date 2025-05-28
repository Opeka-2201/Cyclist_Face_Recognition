import os
from PIL import Image

folder = "mugshots"

# for every file in the folder check for the presence of -n2 or -n3 in the name and remove it
def clean_filenames(folder):
    for filename in os.listdir(folder):
        if "-n2" in filename or "-n3" in filename:
            new_filename = filename.replace("-n2", "").replace("-n3", "")
            os.rename(os.path.join(folder, filename), os.path.join(folder, new_filename))
            print(f"Renamed: {filename} -> {new_filename}")

def remove_duplicates(folder):
    for filename in os.listdir(folder):
        if " 2" in filename:
            os.remove(os.path.join(folder, filename))
            print(f"Removed duplicate file: {filename}")

clean_filenames(folder)
remove_duplicates(folder)