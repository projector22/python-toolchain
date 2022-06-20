# file_path_mapper_example.py

from lib.FilePathMapper import FilePathMapper

scanner = FilePathMapper()
scanner.set_path('my/example/path')
scanner.set_include_hidden(True)
scanner.set_include_empty(False)
scanner.map_path()
scanner.write_map_to_json(pretty_print=True)