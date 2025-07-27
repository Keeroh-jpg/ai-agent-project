import os
import subprocess
from google.genai import types

schema_run_python = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file in the specified working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the Python file to execute. It should be relative to the working directory.",
            )
        }
    )
)



def run_python_file(working_directory, file_path, args=[]):
    working_directory_abs = os.path.abspath(working_directory)
    full_path = os.path.join(working_directory, file_path)
    full_path = os.path.normpath(full_path)
    full_path_abs = os.path.abspath(full_path)
    
    if not full_path_abs.startswith(working_directory_abs):
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
