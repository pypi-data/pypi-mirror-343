import re


def get_files_by_type(image_path, categorized_output, file_types):
    files = categorized_output.splitlines()
    filtered_files = {}
    # Convert file types to lowercase and strip spaces
    file_types = {ft.strip().lower() for ft in file_types}
    for type in file_types:
        extension = type.lower().rsplit('.', 1)[-1] if '.' in type else ''
        filtered_files[extension] = []

    # Regex to extract filenames
    file_pattern = re.compile(r':\t(.+)$')              # Captures everything after the tab

    for line in files:
        match = file_pattern.search(line)
        if match:
            filename = match.group(1)
            extension = filename.lower().rsplit('.', 1)[-1] if '.' in filename else ''

            if f".{extension}" in file_types:
                list_of_files = filtered_files[extension]
                list_of_files.append(filename)
                filtered_files[extension] = list_of_files

    return filtered_files
