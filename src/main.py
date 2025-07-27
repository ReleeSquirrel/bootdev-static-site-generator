import os
import shutil

def main():
    copy_directory("static/", "public/")


def copy_directory(source, destination):
    # First clear the destination to an empty directory
    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.mkdir(destination)

    # Copy all files, subdirectories, etc.
    source_directory_list = os.listdir(source)

    for item in source_directory_list:
        path_to_item = os.path.join(source, item)
        if os.path.isfile(path_to_item):
            path_to_target = os.path.join(destination, item)
            print(f"Copying file {path_to_item} to {path_to_target}")
            shutil.copy(path_to_item, path_to_target)
        else:
            path_to_target = os.path.join(destination, item)
            print(f"Copying directory {path_to_item} to {path_to_target}")
            copy_directory(path_to_item, path_to_target)



main()