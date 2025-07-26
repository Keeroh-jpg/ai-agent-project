import os
from functions.config import MAX_CHARS

def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)
    full_path = os.path.normpath(full_path)
    
    if full_path.startswith(working_directory) is False:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory.'
    if not os.path.isfile(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    

    with open(full_path, "r") as file:
        file_content_string = file.read(MAX_CHARS)
        if len(file.read()) > MAX_CHARS:
            file_content_string = file_content_string[:MAX_CHARS] + f' [...File "{file_path}" truncated to {MAX_CHARS} characters]'

    return file_content_string
