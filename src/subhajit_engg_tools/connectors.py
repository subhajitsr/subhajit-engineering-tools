import psycopg2
import pandas as pd


class Postgres:
    def __init__(
            self,
            host: str,
            database: str,
            user: str,
            password: str
    ):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        try:
            self.conn = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)
            self.conn.autocommit = True
        except Exception as e:
            raise Exception(f"Could not connect to the database. {e} ")

    def insert_records(self,
                       data: list,
                       columns: list,
                       table_name: str,
                       schema: str = "public",
                       ):
        values_str = ",".join(["%s" for col in columns])
        col_str = ",".join([col for col in columns])

        cur = self.conn.cursor()
        data_lst_tuple = [tuple(row.values()) for row in data]
        args = ','.join(cur.mogrify(f"""({values_str})""", i).decode('utf-8') for i in data_lst_tuple)
        sql = f"""insert into {schema}.{table_name} ({col_str}) values {args}"""

        try:
            cur.execute(sql)
        except Exception as e:
            raise Exception(f"Insert failure. {e} ")

        cur.close()

    def execute(self, sql: str):
        cur = self.conn.cursor()
        try:
            cur.execute(sql)
        except Exception as e:
            cur.close()
            raise Exception(f"Exec failure. {e} ")

        cur.close()

    def get_result(self, sql: str):
        return pd.read_sql(sql, con=self.conn)
