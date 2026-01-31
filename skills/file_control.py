import os
import shutil

BASE_DIR = os.getcwd()

def set_base_dir(path):
    global BASE_DIR
    BASE_DIR = path

def create_file(name):
    path = os.path.join(BASE_DIR, name)
    folder_name = os.path.basename(BASE_DIR)
    if os.path.exists(path):
        return f"The file named {name} already exists in the folder {folder_name}"
    open(path, 'w').close()
    return f"A new file named {name} has been created in the folder {folder_name}."


def delete_file(name):
    path = os.path.join(BASE_DIR, name)
    folder_name = os.path.basename(BASE_DIR)
    if not os.path.exists(path):
        return f"I could not find a file named {name}."
    os.remove(path)
    return f"The file named {name} has been successfully deleted from {folder_name}."

def create_folder(name):
    path = os.path.join(BASE_DIR, name)
    folder_name = os.path.basename(BASE_DIR)
    if os.path.exists(path):
        return f"Folder '{name}' already exists."
    os.mkdir(path)
    return f"Folder '{name}' created in the parent folder {folder_name}"

def delete_folder(name):
    path = os.path.join(BASE_DIR, name)
    if not os.path.exists(path):
        return f"Folder '{name}' not found."
    shutil.rmtree(path)
    return f"Folder '{name}' deleted."

def list_items():
    items = os.listdir(BASE_DIR)
    if not items:
        return "The selected folder is empty."
    return (
        f"Here are all the files and folders in the directory {BASE_DIR}:\n"
        + ", ".join(items)
    )
