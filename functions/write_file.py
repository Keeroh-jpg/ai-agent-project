import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a specified file that is within the permitted working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to write content to. It should be relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            )
        }
    )
)


def write_file(working_directory, file_path, content):
    working_directory_abs = os.path.abspath(working_directory)
    full_path = os.path.join(working_directory, file_path)
    full_path = os.path.normpath(full_path)
    full_path_abs = os.path.abspath(full_path)
    
    if not full_path_abs.startswith(working_directory_abs):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory.'
    
    if not os.path.exists(os.path.dirname(full_path)):
        os.makedirs(os.path.dirname(full_path))

    with open(full_path, "w") as file:
        file.write(content)
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written).'