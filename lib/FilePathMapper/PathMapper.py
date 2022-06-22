import os

class PathMapper:
    """This class is a tool for mapping out file and folder structures and returning them in a useable format.

    Args:
        path (str, optional): The path to map out. Defaults to '.' (this directory).
    
    Author:
        Gareth Palmer - https://github.com/projector22, https://gitlab.com/projector22

    Version:
        1.0.0
    """
    def __init__(self, path = '.'):
        """Class constructor.

        Args:
            path (str, optional): The path to map out. Defaults to '.' (this directory).

        Since:
            1.0.0
        """
        self.path = path
        self._file_iterator = None
        self.dir_map = dict()
        self.limit_to_type = None
        self.include_hidden = True
        self.include_empty = True



    def __del__(self):
        """Class deconstructor.
        """
        try:
            self._file_iterator.close()
        except:
            pass



    def set_path(self, path: str) -> object:
        """Set the path to scan and work through.

        Args:
            path (str): Full or relative path.

        Returns:
            object: self - used for method chaining.
        """
        self.path = path
        return self



    def _path_mapper(self, path: str) -> dict:
        """Recursively map out files and folder structure.

        Args:
            path (str): The path to map.

        Returns:
            dict: Mapped out path.
        """
        structure = {
            'dirs': {},
            'files': [],
        }
        if self.include_empty == False:
            if len(list(os.scandir(path))) == 0:
                return {}
        for entry in os.scandir(path):
            if entry.is_dir() == True:
                if self.include_hidden == False:
                    if entry.name.startswith('.'):
                        continue
                structure['dirs'][entry.name] = {}
                structure['dirs'][entry.name] = self._path_mapper(entry.path)
                if self.include_empty == False:
                    if structure['dirs'][entry.name] == {}:
                        del structure[entry.name]
            else:
                structure['files'].append(entry.name)
        return structure



    def map_path(self) -> object:
        """Perform the mapping of the selected path.

        Returns:
            object: self - used for method chaining.
        """
        self.dir_map = self._path_mapper(self.path)
        return self



    def write_map_to_json(self, file_name: str = 'data', pretty_print: bool = False) -> object:
        """Export the completed map to a JSON file.

        Args:
            file_name (str, optional): The name of the file to export to. Extension can be left off. Defaults to 'data'.
            pretty_print (bool, optional): Format the JSON to be more readable. False will leave the JSON at it's most compact. Defaults to False.

        Returns:
            object: self - used for method chaining.
        """
        import json
        if file_name[-5:] != '.json':
            file_name = str(file_name) + '.json'
        with open(file_name, "w") as file:
            if pretty_print:
                json.dump(self.dir_map, file, indent=4)
            else:
                json.dump(self.dir_map, file)
        file.close()
        return self



    def set_limit_to_type(self, limit: str|list = '*') -> object:
        """Set a limit on the type of file to map, if you want to find a file of a certain type or types.

        Args:
            limit (str | list, optional): Either a single file extension, or a list of file extensions. If '*', everything will be listed. Defaults to '*'.

        Todo:
            Build this method & it's required logic in `self._path_mapper()`!!

        Returns:
            object: self - used for method chaining.
        """


        ## Build here


        return self



    def set_include_hidden(self, show_hidden: bool) -> object:
        """Set a flag to include or exclude hidden files.

        Args:
            show_hidden (bool): Whether or not to enable inclusion of hidden files.

        Returns:
            object: self - used for method chaining.
        """
        self.include_hidden = show_hidden
        return self



    def set_include_empty(self, show_empty: bool) -> object:
        """Set a flag to include or exclude empty directories / folders.

        Args:
            show_empty (bool): Whether or not to enable inclusion of empty directories / folders.

        Returns:
            object: self - used for method chaining.
        """
        self.include_empty = show_empty
        return self

