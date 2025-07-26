import os


def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)
    full_path = os.path.normpath(full_path)
    
    if full_path.startswith(working_directory) is False:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory.'
    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory.'
    directory_contents = os.listdir(full_path)
    outputs = []
    for content in directory_contents:
        content_full_path = os.path.join(full_path, content)
        
        if os.path.isfile(content_full_path):
            outputs.append(f"- {content}: file_size={os.path.getsize(content_full_path)} bytes, is_dir=False")
        elif os.path.isdir(content_full_path):
            outputs.append(f"- {content}: file_size={os.path.getsize(content_full_path)} bytes, is_dir=True")

    return "\n".join(outputs)
