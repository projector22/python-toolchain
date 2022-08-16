def add_to_archive(json_data: dict, json_file_name: str, zip_file_name: str):
    """Write the parsed data to JSON, then add it to a zip
    archive.

    Args:
        json_data (dict): The data to write to the JSON file.
        json_file_name (str): The name of the JSON file being written.
        zip_file_name (str): The name of the ZIP archive being created or added to.
    """

    import json
    with open(json_file_name, "w") as file:
        json.dump(json_data, file)
    file.close()

    print("Adding to " + zip_file_name)

    import zipfile
    with zipfile.ZipFile(zip_file_name, mode="a") as archive:
        archive.write(json_file_name)

    import os
    os.remove(json_file_name)
