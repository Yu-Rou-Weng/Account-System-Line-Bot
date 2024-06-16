import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

class postgresDB():
    def __init__(self):
        load_dotenv()
        self.DB_NAME = os.getenv('DB_NAME')
        self.DB_HOST = os.getenv('DB_HOST')
        self.DB_PORT = os.getenv('DB_PORT')
        self.DB_USER = os.getenv('DB_USER')
        self.DB_PASSWD = os.getenv('DB_PASSWD')
        self.conn = None

    def __del__(self):
        if (self.conn is not None):
            self.close()

    def connect(self):
        if self.conn is not None:
            return
        self.conn = psycopg2.connect(
            database=self.DB_NAME,
            user=self.DB_USER,
            password=self.DB_PASSWD,
            host=self.DB_HOST,
            port=self.DB_PORT
        )
        self.conn.autocommit = True
    
    def close(self):
        self.conn.close()
        self.conn = None

    def execute_stmt(self, stmt_format, stmt_args, isSelect):
        ret = []
        with self.conn.cursor() as cur:
            cur.execute(stmt_format, stmt_args)
            if isSelect:
                row = cur.fetchone()
                while (row is not None):
                    ret.append(row)
                    row = cur.fetchone()
        return ret