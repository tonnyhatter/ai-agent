import os
import subprocess
from config import MAX_CHARACTERS

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

def get_file_content(working_directory, file_path):
    try:
        absolute_path = os.path.abspath(os.path.join(working_directory, file_path))
        if not absolute_path.startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(absolute_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(absolute_path, "r") as f:
            file_contents_string = f.read(MAX_CHARACTERS)
            if len(file_contents_string) == MAX_CHARACTERS:
                file_contents_string += '[...File "{file_path}" truncated at 10000 characters]'
        return file_contents_string
    except PermissionError as e:
        return f"Error: permission denied for '{file_path}' - {str(e)}"
    except FileNotFoundError as e:
        return f"Error: File '{file_path}' not found - {str(e)}"
    except OSError as e:
        return f"Error: An OS Error occurred - {str(e)}"
    except Exception as e:
        return f"Error: An unexpected error occurred - {str(e)}"

def write_file(working_directory, file_path, content):
    try:
        absolute_path = os.path.abspath(os.path.join(working_directory, file_path))
        if not absolute_path.startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        directory_path = os.path.dirname(absolute_path)
        if not os.path.exists(directory_path):
            os.path.makedirs(directory_path)
        with open(absolute_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except PermissionError as e:
        return f"Error: permission denied for '{file_path}' - {str(e)}"
    except FileNotFoundError as e:
        return f"Error: File '{file_path}' not found - {str(e)}"
    except OSError as e:
        return f"Error: An OS Error occurred - {str(e)}"
    except Exception as e:
        return f"Error: An unexpected error occurred - {str(e)}"

def run_python_file(working_directory, file_path, args=[]):
    try:
        absolute_path = os.path.abspath(os.path.join(working_directory, file_path))
        if not absolute_path.startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(absolute_path):
            return f'Error: File "{file_path}" not found.'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
        cmd = ["python3", file_path] + args
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=working_directory, timeout=30)
        if result.returncode != 0:
            return f"STDOUT: {result.stdout} \nSTDERR: {result.stderr} \nProcess exited with code {result.returncode}"
        if not result.stdout and not result.stderr:
            return f"No output produced."
        return f"STDOUT: {result.stdout} \nSTDERR: {result.stderr}"
    except Exception as e:
        return f"Error: executing Python file: {e}"