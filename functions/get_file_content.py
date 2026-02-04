import os
from .config import MAX_FILE_SIZE

def get_file_content(working_directory, file_path):
    working_directory = os.path.abspath(working_directory)
    full_directory = os.path.abspath(os.path.join(working_directory, file_path))

    if not full_directory.startswith(working_directory):
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(full_directory):
        return  f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(full_directory, "r") as f:
            file_content_string = f.read()

        if len(file_content_string) > MAX_FILE_SIZE:
            file_content_string = file_content_string[:MAX_FILE_SIZE] + f'[...File "{file_path}" truncated at {MAX_FILE_SIZE} characters]'
        return file_content_string
    except Exception as e:
        return f"Error: {e}"
