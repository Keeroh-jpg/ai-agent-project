import os

def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)
    full_path = os.path.normpath(full_path)
    
    if full_path.startswith(working_directory) is False:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory.'
    
    if not os.path.exists(os.path.dirname(full_path)):
        os.makedirs(os.path.dirname(full_path))

    with open(full_path, "w") as file:
        file.write(content)
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written).'