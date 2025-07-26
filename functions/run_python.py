import os
import subprocess
import sys


def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.join(working_directory, file_path)
    full_path = os.path.normpath(full_path)
    
    if full_path.startswith(working_directory) is False:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory.'
    if not os.path.isfile(full_path):
        return f'Error: File "{file_path}" not found.'
    if not full_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    

    
    try:
        result = subprocess.run(["python", file_path] + args, capture_output=True, cwd=working_directory, timeout=30, text=True)
        if result.returncode != 0:
            return f'Error: Process exited with code {result.returncode}'
        result_output = f'STDOUT: {(result.stdout)}'
        if result.stderr:
            result_output += f'\nSTDERR: {(result.stderr)}'
        if not result_output.strip():
            result_output = 'No output produced.'
    except Exception as e:
        return f'Error: executing Python file: {e}'

    
    
    return result_output
