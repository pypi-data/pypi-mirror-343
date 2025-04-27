import os

def list_current_directory(current_dir, prefix="", current_depth=0, max_depth=1):
    if not os.path.isdir(current_dir):
        print(f"{current_dir} is not a valid directory")
        return

    items = sorted(os.listdir(current_dir))
    items = [item for item in items if not item.startswith('.') and not should_exclude(item)]

    for index, item in enumerate(items):
        full_path = os.path.join(current_dir, item)
        is_last = index == len(items) - 1
        connector = "└── " if is_last else "├── "

        if os.path.isdir(full_path):
            print(f"{prefix}{connector}{item}/")
            if current_depth < max_depth:
                extension = "    " if is_last else "│   "
                list_current_directory(full_path, prefix + extension,
                                       current_depth + 1, max_depth)
        elif os.path.isfile(full_path):
            print(f"{prefix}{connector}{item}")

def should_exclude(item):
    return (
        item == '__pycache__' or
        item.endswith(('.pyc', '.pyo', '.dist-info', '.egg-info')) or
        item in ('pyvenv.cfg', 'Scripts', 'bin', 'Lib')
    )

def list_multiple_directories(base_path, directories_to_check, max_depth=1):
    for dir_name in directories_to_check:
        full_path = os.path.join(base_path, dir_name)
        if os.path.exists(full_path):
            print(f"\n{dir_name}/")
            list_current_directory(full_path, prefix="    ",
                                   current_depth=0, max_depth=max_depth)
        else:
            print(f"-- {dir_name}/ (not found)")

# === Example usage ===
if __name__ == "__main__":
    dirs = ["."]  # Add more directories if needed
    list_multiple_directories(os.getcwd(), dirs, max_depth=4)
