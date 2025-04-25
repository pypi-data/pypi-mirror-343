import os
import sys
from .templates import get_main_template, get_utils_template, get_readme_template, get_server_template, get_client_template

def create_structure(structure_type: str = "default") -> None:
    root_dir = os.getcwd()

    if structure_type == "default":
        structure = {
            "src": {
                "utils.py": get_utils_template(),
            },
            "example.py": get_main_template(),
            "README.md": get_readme_template(),
        }
    elif structure_type == "app":
        structure = {
            "src": {
                "utils.py": get_utils_template(),
            },
            "apps": {
                "server_app.py": get_server_template(),
                "client_app.py": get_client_template(),
            },
            "example.py": get_main_template(),
            "TUTORIAL.md": get_readme_template(),
        }
    else:
        print(f"Unknown structure type: {structure_type}")
        sys.exit(1)

    for folder, files in structure.items():
        path = os.path.join(root_dir, folder)
        if isinstance(files, dict):  # If folder contains files
            os.makedirs(path, exist_ok=True)
            for file, content in files.items():
                file_path = os.path.join(path, file)
                with open(file_path, "w") as f:
                    f.write(content)
        else:  # Single file at the root
            with open(os.path.join(root_dir, folder), "w") as f:
                f.write(files)

    print(f"Project structure for {structure_type} created successfully in {root_dir}.")

def create_structure_app():
    pass

def main():
    if len(sys.argv) < 2:
        print("Usage: msi <command> [options]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "init":
        structure_type = sys.argv[2] if len(sys.argv) > 2 else "default"
        create_structure(structure_type)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

