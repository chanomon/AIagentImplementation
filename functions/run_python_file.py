import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    working_directory = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not full_path.startswith(working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(full_path): 
        return f'Error: File "{file_path}" not found.'

    if not full_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        command = ["python",full_path] + args
        completed_process = subprocess.run(
            command,
            cwd = working_directory,
            capture_output=True,
            text = True,
            timeout=30
        )
        output_parts = []
        if completed_process.stdout:
            output_parts.append(f'STDOUT:\n{completed_process.stdout.strip()}')
        if completed_process.stderr:
            output_parts.append(f'STDERR:\n{completed_process.stderr.strip()}')
        if not completed_process.stdout and not completed_process.stderr:
            output_parts.append('No output produced.')

        #if completed_proces.returncode == 0:
        #    return f'STDOUT:{completed_proces.stdout} STDERR:{completed_proces.stderr}' 
        if completed_process.returncode != 0:
            #return f'Process exited with code {completed_proces.returncode}' 
            output_parts.append(f'Process exited with code {completed_process.returncode}')
        return '\n'.join(output_parts)
    except Exception as e:
        return f"Error: {e}"
