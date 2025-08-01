import os

def get_files_info(working_directory, directory="."):
    try:
        absolute_path = os.path.abspath(os.path.join(working_directory, directory))
        if not absolute_path.startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(absolute_path):
            return f'Error: "{directory}" is not a directory'
        files_and_dirs = os.listdir(absolute_path)
        item_list = []
        for item in files_and_dirs:
            full_path = os.path.join(absolute_path, item)
            item_size = os.path.getsize(full_path)
            is_dir = os.path.isdir(full_path)
            item_list.append(f"- {item}: file_size={item_size} bytes, is_dir={is_dir}")
        return "\n".join(item_list)
    except PermissionError as e:
        return f'Error: Permission denied for "{directory}" - {str(e)}'
    except FileNotFoundError as e:
        return f'Error: Directory "{directory}" not found - {str(e)}'
    except OSError as e:
        return f'Error: An OS error occurred - {str(e)}'
    except Exception as e:
        return f'Error: An unexpected error occurred - {str(e)}'