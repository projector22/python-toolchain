import pyodbc
from sys import exit

class MDB_SQL:
    """Class for interacting with an Microsoft Access Database (mdb, accdb).

    Args:
        db (str): The database name.
        pw (str): The database password if required. Defaults to "".

    Author:
        Gareth Palmer @evangeltheology

    Version:
        1.0.0

    Since:
        3.26.4
    """

    def __init__(
        self, 
        db: str, 
        pw: str = ""
    ) -> None:
        self.db = db
        self.pw = pw
        self.driver = "Microsoft Access Driver (*.mdb, *.accdb)"

        self.debug = False

        self.connection = pyodbc.connect(r"Driver={%s};DBQ=%s;PWD=%s" % (self.driver, self.db, self.pw))
        self.cursor = self.connection.cursor()

        self.selected_table = None

        self.tables = []
        for row in self.cursor.tables():
            if "MSys" in row.table_name:
                continue
            self.tables.append(row.table_name)

        self.values = None



    def _prepare_where(self, where: dict) -> str:
        """Prepare the queries, handling things like, not equal or IN

        Args:
            where (dict): The parsed where clauses.

        Returns:
            str: Prepared WHERE string

        Since:
            3.26.4
        """
        like = lambda a : a[-5:] == " LIKE"
        not_like = lambda a : a[-9:] == " NOT LIKE"
        ## Null testing seems to break this, @todo fix
        is_null = lambda a : a[-8:] == " IS NULL"
        is_not_null = lambda a : a[-12:] == " IS NOT NULL"
        is_not_equal = lambda a : a[-3:] == " <>"
        greater_than = lambda a : a[-2:] == " >"
        less_than = lambda a : a[-2:] == " <"
        greater_equals_to = lambda a : a[-3:] == " >="
        less_equals_to = lambda a : a[-3:] == " <="
        is_in = lambda a : a[-3:] == " IN"
        is_not_in = lambda a : a[-7:] == " NOT IN"

        where_str = " WHERE "
        wheres = []
        for key in where:
            if like(key) or not_like(key):
                wheres.append(key + " ?")
                self.values.append(where[key])
            elif is_not_equal(key) or greater_than(key) or less_than(key):
                wheres.append(key + "?")
                self.values.append(where[key])
            elif greater_equals_to(key) or less_equals_to(key):
                wheres.append(key + "?")
                self.values.append(where[key])
            elif is_in(key) or is_not_in(key):
                set_where = key + " ("
                q_marks = []
                for value in where[key]:
                    self.values.append(value)
                    q_marks.append("?")
                set_where += ",".join(q_marks)
                set_where += ")"
                wheres.append(set_where)
            else:
                wheres.append(key + "=?")
                self.values.append(where[key])
        where_str += " AND ".join(wheres)
        return where_str



    def execute(
        self, 
        sql: str
    ) -> int:
        """A basic catch all SQL executor, for performing all but SELECT queries.

        Args:
            sql (str): SQL string to parse.

        Returns:
            int: The number of lines affected.

        Since:
            3.26.4
        """

        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except pyodbc.Error as e:
            print("Could not execute command `{}`".format(sql))
            if self.debug == True:
                print("Error message:", e)
        finally:
            return self.cursor.rowcount



    def table(
        self, 
        table: str
    ) -> object:
        """Set the table to apply sql queries and commands on.

        Args:
            table (str): The selected table.

        Returns:
            object: This current object for method chaining.

        Since:
            3.26.4
        """
        if table not in self.tables:
            print("Error - selected table `{}` not in database".format(table))
            exit()
            
        self.selected_table = table
        return self



    def insert(
        self, 
        fields: dict
    ) -> int:
        """Perform an SQL INSERT command on the previously selected table.

        Args:
            fields (dict): Key -> Value pairs to insert.

        Returns:
            int: The number of lines affected.

        Since:
            3.26.4
        """
        if self.selected_table == None:
            print("Error - no table selected")
            exit()

        sql = r"INSERT INTO `%s` " % self.selected_table
        keys = []
        values = []
        q_marks = []
        for key in fields:
            keys.append(key)
            q_marks.append('?')
            values.append(fields[key])

        sql += "(`" + "`,`".join(keys) + "`) VALUES "
        sql += "(" + ",".join(q_marks) + ")"

        try:
            self.cursor.execute(sql, *values)
            self.connection.commit()
        except pyodbc.Error as e:
            print("Could not insert fields into `{}`".format(self.selected_table))
            if self.debug == True:
                print("SQL:", sql)
                print("fields:", fields)
                print("Error message:", e)
        finally:
            return self.cursor.rowcount



    def update(
        self, 
        fields: dict, 
        where: dict
    ) -> int:
        """Perform an SQL UPDATE command on the previously selected table.

        Args:
            fields (dict): The fields to update.
            where (dict): The conditions of the update.

        Returns:
            int: The number of lines affected.
        """
        if self.selected_table == None:
            print("Error - no table selected")
            exit()

        sql = r"UPDATE `%s` SET " % self.selected_table
        keys = []
        values = []
        for key in fields:
            keys.append(r"`%s`=?" % key)
            values.append(fields[key])
        sql += ", ".join(keys)
        sql += " WHERE "

        # @todo - Add in support for "OR"
        wheres = []
        for key in where:
            wheres.append("`{}`=?".format(key))
            values.append(where[key])
        sql += " AND ".join(wheres)

        try:
            self.cursor.execute(sql, *values)
            self.connection.commit()
        except pyodbc.Error as e:
            print("Could not updates fields on `{}`".format(self.selected_table))
            if self.debug == True:
                print("SQL:", sql)
                print("fields:", fields)
                print("where:", where)
                print("Error message:", e)
        finally:
            return self.cursor.rowcount



    def delete(
        self, 
        where: dict
    ) -> int:
        """Delete from the previously selected database.

        Args:
            where (dict): The where clause of the delete statement.

        Returns:
            int: The number of lines affected.

        Since:
            3.26.4
        """
        if self.selected_table == None:
            print("Error - no table selected")
            exit()

        sql = r"DELETE FROM `%s` WHERE " % self.selected_table

        values = []
        wheres = []
        for key in where:
            wheres.append("{}=?".format(key))
            values.append(where[key])
        sql += " AND ".join(wheres)

        try:
            self.cursor.execute(sql, *values)
            self.connection.commit()
        except pyodbc.Error as e:
            print("Could not delete fields on `{}`".format(self.selected_table))
            if self.debug == True:
                print("SQL:", sql)
                print("where:", where)
                print("Error message:", e)
        finally:
            return self.cursor.rowcount



    def _perform_select(
        self, 
        fields: list|str, 
        where: dict = None, 
        order_by: str = None
    ) -> str:
        """Handle the generation of an SQL select string.

        Args:
            fields (list | str): Fields to select.
            where (dict, optional): The where clause of the SQL string. Defaults to None.
            order_by (str, optional): The "Order By" clause of the SQL string. Defaults to None.

        Returns:
            str: fully formed SQL string

        Since:
            3.26.4
        """

        sql = "SELECT "

        columns = []
        if type(fields) == list:
            for field in fields:
                columns.append(field)
            sql += "`" + "`, `".join(columns) + "`"
        else:
            sql += fields
        
        sql += " FROM {}".format(self.selected_table)

        self.values = []
        if where is not None and len(where) > 0:
            sql += self._prepare_where(where)

        if order_by is not None:
            sql += " ORDER BY {}".format(order_by)

        return sql



    def select_all(
        self, 
        fields: list|str = '*', 
        where: dict = None, 
        order_by: str = None, 
        limit: int = None
    ) -> object:
        """Perform an SQL SELECT all statement, fetching all, 
        or many (if a limit is set) values based on the params.

        Args:
            fields (list | str, optional): The fields to select. Defaults to '*'.
            where (dict, optional): The where clause of the select. Defaults to None.
            order_by (str, optional): The order by clause. Defaults to None.
            limit (int, optional): The limit by cluase. Defaults to None.

        Returns:
            object: The results of the search.

        Since:
            3.26.4
        """

        if self.selected_table == None:
            print("Error - no table selected")
            exit()

        sql = self._perform_select(fields, where, order_by)

        try:
            if len(self.values) > 0:
                self.cursor.execute(sql, *self.values)
            else:
                self.cursor.execute(sql)

            if limit is not None:
                return self.cursor.fetchmany(limit)
            else:
                return self.cursor.fetchall()
        except pyodbc.Error as e:
            print("Could not perform select on `{}`".format(self.selected_table))
            if self.debug == True:
                print("SQL:", sql)
                print("where:", where)
                print("Error message:", e)
            return {}



    def select_one(
        self, 
        fields: list|str = '*', 
        where: dict = None
    ) -> object:
        """Perform an SQL SELECT one statement, fetching a single result.

        Args:
            fields (list | str, optional): The fields to select. Defaults to '*'.
            where (dict, optional): The where clause of the select. Defaults to None.

        Returns:
            object: The results of the search.

        Since:
            3.26.4
        """
        if self.selected_table == None:
            print("Error - no table selected")
            exit()
        
        sql = self._perform_select(fields, where)

        try:
            if len(self.values) > 0:
                self.cursor.execute(sql, *self.values)
            else:
                self.cursor.execute(sql)
            return self.cursor.fetchone()
        except pyodbc.Error as e:
            print("Could not perform select on `{}`".format(self.selected_table))
            if self.debug == True:
                print("SQL:", sql)
                print("where:", where)
                print("Error message:", e)
            return {}
