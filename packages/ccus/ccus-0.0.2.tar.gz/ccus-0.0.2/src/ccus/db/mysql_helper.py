import pymysql
from dbutils.pooled_db import PooledDB
from contextlib import contextmanager
from dataclasses import dataclass


@dataclass
class MySQLConfig:
    host: str = "localhost"
    port: int = 3306
    user: str = "root"
    password: str = "123456"
    database: str = "kygl"


class MySQLHelper:
    def __init__(self, config: MySQLConfig):
        self.pool = PooledDB(
            creator=pymysql,
            maxconnections=20,
            mincached=2,
            maxcached=5,
            blocking=True,
            ping=0,
            host=config.host,
            port=config.port,
            user=config.user,
            password=config.password,
            database=config.database,
            charset='utf8mb4',
            autocommit=False
        )
        print(f"连接到服务器：{config.host}:{config.port}     账号:{config.user}")

    @contextmanager
    def get_conn_cursor(self):
        """
        上下文管理器，自动获取和释放连接与游标
        """
        conn = self.pool.connection()
        cursor = conn.cursor()
        try:
            yield conn, cursor
        finally:
            cursor.close()
            conn.close()

    def fetchone(self, sql, *args):
        with self.get_conn_cursor() as (_, cursor):
            cursor.execute(sql, args)
            return cursor.fetchone()

    def fetchall(self, sql, *args):
        with self.get_conn_cursor() as (_, cursor):
            cursor.execute(sql, args)
            return cursor.fetchall()

    def execute(self, sql, *args):
        """
        执行插入/更新/删除操作
        """
        with self.get_conn_cursor() as (conn, cursor):
            cursor.execute(sql, args)
            conn.commit()
            return cursor.rowcount

    def insert(self, sql, *args):
        """
        插入数据并返回自增ID
        """
        with self.get_conn_cursor() as (conn, cursor):
            cursor.execute(sql, args)
            conn.commit()
            return cursor.lastrowid

    def execute_many(self, sql, arg_list):
        """
        批量执行SQL
        """
        with self.get_conn_cursor() as (conn, cursor):
            cursor.executemany(sql, arg_list)
            conn.commit()
            return cursor.rowcount

    def transaction(self, sql_list):
        """
        执行多条SQL语句，手动事务控制
        """
        with self.get_conn_cursor() as (conn, cursor):
            try:
                for sql in sql_list:
                    cursor.execute(sql)
                conn.commit()
                return True
            except Exception as e:
                conn.rollback()
                return e
