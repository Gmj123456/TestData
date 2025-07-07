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

    def fetch_contact_email(self, sys_user_name: str = None):
        """
        获取顾问建联邮箱列表或根据用户名获取邮箱列表

        Args:
            sys_user_name: 用户名（可选），若提供则返回对应邮箱列表

        Returns:
            若提供用户名：该用户的邮箱列表（可能为空）
            若未提供用户名：所有邮箱列表
        """
        try:
            with connect(**self.config) as connection:
                with connection.cursor() as cursor:
                    if sys_user_name:
                        # 根据顾问名称查询邮箱列表
                        query = """
                        SELECT contact_email 
                        FROM store_user_contact_email 
                        WHERE sys_user_name = %s
                        """
                        cursor.execute(query, (sys_user_name,))
                        return [row[0] for row in cursor.fetchall() if row[0] is not None]
                    else:
                        # 查询所有邮箱列表
                        cursor.execute("SELECT contact_email FROM store_user_contact_email")
                        return [row[0] for row in cursor.fetchall() if row[0] is not None]
        except Error as e:
            print(f"数据库错误: {e}")
            return []


    # 获取类目
    def fetch_category(self):
        """获取私有网红类目列表，返回 Python 列表"""
        try:
            with connect(**self.config) as connection:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT like_tag_name FROM store_tags")
                    return [row[0] for row in cursor.fetchall() if row[0] is not None]
        except Error as e:
            print(f"数据库错误: {e}")
            return []