import unittest
from get_mysql_data.get_mysql_data_kolbox import DataRepository

class TestDataRepository(unittest.TestCase):
    def setUp(self):
        """初始化 DataRepository 实例"""
        self.repo = DataRepository()

    def test_fetch_countries(self):
        """测试获取国家列表"""
        countries = self.repo.fetch_countries()
        self.assertIsInstance(countries, list, "返回结果应为列表")
        print(countries)
        # 可选：根据数据库实际情况添加更具体的断言
        # self.assertIn("China", countries)

    def test_fetch_brands(self):
        """测试获取品牌列表"""
        brands = self.repo.fetch_brands()
        self.assertIsInstance(brands, list, "返回结果应为列表")
        print(brands)
        # 可选：根据数据库实际情况添加更具体的断言
        # self.assertIn("BrandA", brands)

if __name__ == '__main__':
    unittest.main()
