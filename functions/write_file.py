import os


def write_file(working_directory, file_path, content):
    working_directory = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not full_path.startswith(working_directory):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(os.path.dirname(full_path)):
        try:
            os.makedirs(os.path.dirname(full_path))
        except Exception as e:
            return f"Error: {e}"
    with open(full_path, "w") as f:
        f.write(content)
        print(f'Successfully wrote to "{file_path}" ({len(content)} characters written)')

