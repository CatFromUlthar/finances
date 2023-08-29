import sqlite3


class DataBaseInteractor:
    def __init__(self, db_name: str):
        self._db_name = db_name

    def __repr__(self):
        return f'DataBaseInteractor("{self._db_name}")'

    def create_table(self, table_name: str, **columns):
        columns_list = [f'{c} {columns[c].upper()}' for c in columns]
        columns_query = ', '.join(columns_list)

        main_query = f"""CREATE TABLE IF NOT EXISTS {table_name} ({columns_query})"""

        with sqlite3.connect(self._db_name) as con:
            cur = con.cursor()
            cur.execute(main_query)

    def get_data(self, table_name: str, *columns, **params):
        columns_query = ', '.join(columns)

        params_list = []

        for p in params:
            if params[p].__class__ == str:
                params_list.append(f"{p} = \'{params[p]}\'")
            else:
                params_list.append(f"{p} = {params[p]}")
        params_query = ' and '.join(params_list)

        if params_query:
            main_query = f'SELECT {columns_query} from {table_name} WHERE {params_query}'
        else:
            main_query = f'SELECT {columns_query} from {table_name}'

        with sqlite3.connect(self._db_name) as con:
            cur = con.cursor()
            cur.execute(main_query)
            result = cur.fetchall()
            return result

    def add_data(self, table_name: str, **data):
        keys_list = [d for d in data]
        keys_query = ', '.join(keys_list)

        values_list = []
        for d in data:
            if data[d].__class__ == str:
                values_list.append(f"\'{data[d]}\'")
            else:
                values_list.append(f"{data[d]}")
        values_query = ', '.join(values_list)

        main_query = f'INSERT INTO {table_name} ({keys_query}) values ({values_query})'

        with sqlite3.connect(self._db_name) as con:
            cur = con.cursor()
            cur.execute(main_query)
