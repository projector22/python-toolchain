# python-toolchain

A number of self written python tools for building out personal projects

## PathMapper

PathMapper is a tool for mapping out files and folders within a defined directory.

### Added

2022-06-20

### Example

```python3
# file_path_mapper_example.py

from lib.FilePathMapper.PathMapper import PathMapper

scanner = PathMapper()
scanner.set_path('my/example/path')
scanner.set_include_hidden(True)
scanner.set_include_empty(False)
scanner.map_path()
scanner.write_map_to_json(pretty_print=True)
```

## ODBC CRUD

Tool for interfacing with a MS Access database (.mdb, .accdb) using the ODBC driver. Allows the full Create, Read, Update & Detele. Generally Linuxy systems don't have an open source ODBC driver for MS Access databases, therefore this tool is primarily for the Windows environment.

### Added

2022-06-22

### Requirements

`pyodbc`

### Example

```python3
# odbc_crud_example.py

from lib.ODBC_CRUD.ODBC_CRUD import MDB_SQL

mdb = MDB_SQL()
data = mdb.table('example_table').select_all(
    fields=[
        "field_a",
        "field_b",
    ],
    where={
        "field": "value",
        "field2": "value2",
    },
    order_by="field2 ASC",
    limit=5,
)
data = mdb.table('example_table').select_one(
    fields=[
        "field_a",
        "field_b",
    ],
    where={
        "field": "value",
        "field2": "value2",
    },
)

mdb.execute("SELECT * FROM `example_table`")

mdb.table('example_table').insert(
    fields={
        "field": "value",
        "field2": "value2",
    }
)

mdb.table('example_table').update(
    fields={
        "field": "value",
    },
    where={
        "field2": "value2",
    },
)

mdb.table('example_table').delete(
    where={
        "field": "value",  
    }
)
```

## Misc Functions

### `add_leading_zero`

#### Added

2022-08-16

#### Example

```python3
from lib.Misc.add_leading_zero import add_leading_zero

print(add_leading_zero(5))
print(add_leading_zero(5, 2))
print(add_leading_zero(0, 1))
print(add_leading_zero(12))
print(add_leading_zero('12'))
print(add_leading_zero('cheese'))
```

### `add_to_archive`

#### Added

2022-08-16

#### Example

```python3
from lib.Misc.add_to_archive import add_to_archive

data = {
    "cheese": [
        "cake", "mouse"
    ],
    "bacon": True
}

add_to_archive(data, "my_json_file.json", "example_file_name.zip")
```

## Attribution

Gareth Palmer ([Gitlab](https://gitlab.com/projector22), [Github](https://github.com/projector22))
