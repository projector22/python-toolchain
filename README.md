# python-toolchain

A number of self written python tools for building out personal projects

## FilePathMapper

FilePathMapper is a tool for mapping out files and folders within a defined directory.

### Example

```python3
# file_path_mapper_example.py

from lib.FilePathMapper import FilePathMapper

scanner = FilePathMapper()
scanner.set_path('my/example/path')
scanner.set_include_hidden(True)
scanner.set_include_empty(False)
scanner.map_path()
scanner.write_map_to_json(pretty_print=True)
```

## Attribution

Gareth Palmer ([Gitlab](https://gitlab.com/projector22), [Github](https://github.com/projector22))
