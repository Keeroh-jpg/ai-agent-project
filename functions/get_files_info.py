import os


def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)
    if os.path.abspath(directory) not in working_directory:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory.'
    if not os.path.isdir(directory):
        return f'Error: "{directory}" is not a directory.'
    directory_contents = os.listdir(full_path)
    outputs = []
    for content in directory_contents:
        if os.path.isfile(content):
            outputs.append(f"- {content}: file_size={os.path.getsize(content)}, is_dir=False")
        elif os.path.isdir(content):
            outputs.append(f"- {content}: file_size={os.path.getsize(content)}, is_dir=True")

    return "\n".join(outputs)
