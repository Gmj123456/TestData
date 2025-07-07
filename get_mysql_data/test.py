import pytest
from get_mysql_data.get_mysql_data_kolbox import DataRepository

@pytest.fixture(scope="function")
def repo():
    """创建 DataRepository 实例的 fixture"""
    return DataRepository()

class TestDataRepository:
    def test_fetch_countries(self, repo):
        """测试获取国家列表"""
        countries = repo.fetch_countries()
        assert isinstance(countries, list), "返回结果应为列表"

    def test_fetch_brands(self, repo):
        """测试获取品牌列表"""
        brands = repo.fetch_brands()
        print(brands)
        assert isinstance(brands, list), "返回结果应为列表"

    def test_fetch_contact_email_list(self, repo):
        """测试获取所有联系人邮箱列表"""
        emails = repo.fetch_contact_email()
        print(emails)
        assert isinstance(emails, list), "返回结果应为列表"
        if emails:
            assert isinstance(emails[0], str), "列表元素应为字符串"

    @pytest.mark.parametrize("test_username", ["gw1"])
    def test_fetch_contact_email_by_username(self, repo, test_username):
        """测试根据用户名获取邮箱列表"""
        emails = repo.fetch_contact_email(test_username)
        print(emails)
        assert isinstance(emails, list), "返回结果应为列表"
        if emails:
            assert isinstance(emails[0], str), "列表元素应为字符串"


    def test_fetch_category(self, repo):
        """测试获取分类列表"""
        categories = repo.fetch_category()
        print(categories)
        assert isinstance(categories, list), "返回结果应为列表"