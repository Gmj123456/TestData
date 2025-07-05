from mysql.connector import connect, Error
from .db_config import DB_CONFIG

class DataRepository:
    def __init__(self):
        self.config = DB_CONFIG

    def fetch_countries(self):
        """获取国家列表，返回 Python 列表"""
        try:
            with connect(**self.config) as connection:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT country FROM country")
                    return [row[0] for row in cursor.fetchall() if row[0] is not None]
        except Error as e:
            print(f"数据库错误: {e}")
            return []

    def fetch_brands(self):
        """获取品牌列表，返回 Python 列表"""
        try:
            with connect(**self.config) as connection:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT brand_name FROM kol_brand")
                    return [row[0] for row in cursor.fetchall() if row[0] is not None]
        except Error as e:
            print(f"数据库错误: {e}")
            return []