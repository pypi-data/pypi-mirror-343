import os

def delete_contents(path):
    for root, dirs, files in os.walk(path, topdown=False):  # Traverse from bottom-up to delete files first
        for file in files:
            if file == "__init__.py":
                continue
            file_path = os.path.join(root, file)
            os.remove(file_path)

        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            if not os.listdir(dir_path):  # If directory is empty, leave it intact
                continue


if __name__ == "__main__":
    logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lsvm_logs_2025")
    if os.path.isdir(logs_dir):
        delete_contents(logs_dir)
        print(f"Cleared contents of '{logs_dir}' except for '__init__.py' files and folders.")
    else:
        print(f"Directory '{logs_dir}' does not exist.")
