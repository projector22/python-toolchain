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