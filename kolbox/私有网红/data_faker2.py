import random
import string
from faker import Faker
from faker.providers import BaseProvider
import pandas as pd  # 用于导出Excel

from get_mysql_data.get_mysql_data import DataRepository

# 初始化Faker
faker = Faker()


# 创建存储库实例
repo = DataRepository()

class SocialMediaProvider(BaseProvider):
    """社交媒体账号生成器，符合各平台规则"""

    # 从数据库中取值：国家、品牌、建联邮箱、类目
    def country(self):
        """生成随机国家/地区"""
        country_list = repo.fetch_countries_as_list()
        return random.choice(country_list)

    def brand(self):
        """生成随机品牌"""

        brand_list = repo.fetch_brands_as_list()
        return random.choice(brand_list)


    def gender(self):
        """生成随机性别"""
        return random.choice(['男', '女'])

    def platform(self):
        """随机选择平台（带权重）"""
        return random.choices(["IG", "YT", "TK"], weights=[20, 40, 40], k=1)[0]

    def content(self, platform):
        """根据平台生成对应内容类型"""
        content_map = {
            "IG": ["IG Reel", "IG Story", "IG Reel"],
            "YT": ["YT 专题5-10min", "YT 插播2-3min"],
            "TK": ["TikTok视频", "TK直播"]
        }
        return random.choice(content_map[platform])

    def label(self):
        """生成随机标签"""
        return random.choice(["hometip", "decoration", "setupreview", "hacks"])



    def generate_tiktok_username(self):
        """生成符合TikTok规则的用户名（只含字母数字下划线英文点）"""
        allowed = string.ascii_letters + string.digits + '_.'  # 只允许字母、数字、下划线和点
        length = random.randint(2, 24)

        while True:
            username = ''.join(random.choice(allowed) for _ in range(length))
            if not username.endswith('.'):  # 确保句点不在结尾
                return username

    def generate_youtube_username(self):
        """生成符合YouTube规则的用户名（只含字母数字下划线英文点）"""
        allowed = string.ascii_letters + string.digits + '_.'  # 只允许字母、数字、下划线和点
        length = random.randint(1, 60)

        # 移除emoji支持，只使用允许的字符
        return ''.join(random.choice(allowed) for _ in range(length))

    def generate_instagram_username(self):
        """生成符合Instagram规则的用户名（只含字母数字下划线英文点）"""
        first_chars = string.ascii_letters + '_'  # 首字符只能是字母或下划线
        allowed = string.ascii_letters + string.digits + '_.'  # 只允许字母、数字、下划线和点
        length = random.randint(3, 30)

        username = [random.choice(first_chars)]
        username.extend(random.choice(allowed) for _ in range(length - 2))
        username.append(random.choice(allowed.replace('.', '')))  # 最后一个字符不能是点

        return ''.join(username)

    def generate_email(self):
        """生成随机合法邮箱"""
        username = ''.join(random.choice(string.ascii_letters + string.digits)
                           for _ in range(random.randint(5, 12)))
        domain = random.choice(["gmail.com", "yahoo.com", "hotmail.com", "163.com", "qq.com", "sina.com"])
        return f"{username}@{domain}"

    def generate_random_note(self):
        """生成简单随机备注（数字+文字）"""
        phrases = [
            "合作意向高", "新账号", "高转化", "需跟进", "女性受众",
            "家居领域", "美妆博主", "价格可议", "数据稳定", "待审核",
            "回复快", "粉丝活跃", "有电商经验", "适合长期合作", "内容优质"
        ]
        number = random.randint(100, 999)
        return f"{random.choice(phrases)}{number}"

    def generate_account(self, platform=None):
        """生成单个账号，可指定平台"""
        if not platform:
            platform = self.platform()

        platform_names = {"TK": "TikTok", "IG": "Instagram", "YT": "YouTube"}
        platform_name = platform_names.get(platform, "未知平台")

        if platform == "TK":
            username = self.generate_tiktok_username()
        elif platform == "IG":
            username = self.generate_instagram_username()
        elif platform == "YT":
            username = self.generate_youtube_username()  # 移除emoji选项
        else:
            username = "invalid_user"

        email = self.generate_email()
        jianlian_email = random.choice(["bbbb@qq.com", "19999999@qq.com"])
        signing_fee = round(random.uniform(1000, 10000), 2)
        note = self.generate_random_note()

        # 类目选项和生成逻辑
        category_options = ["美妆个护", "服装配饰"]

        # 确保至少有一个类目
        category_count = random.randint(1, 5)
        selected_categories = random.choices(category_options, k=category_count)

        # 填充5个类目字段，不足的用空字符串补全
        category_fields = selected_categories + [''] * (5 - len(selected_categories))
        random.shuffle(category_fields)

        return {
            "平台": platform_name,
            "平台代码": platform,
            "账号": username,
            "性别": self.gender(),
            "邮箱": email,
            "国家": self.country(),
            "内容": self.content(platform),
            "个性化标签": self.label(),
            "签约费用": signing_fee,
            "建联邮箱": jianlian_email,
            "备注": note,
            "类目1": category_fields[0],
            "类目2": category_fields[1],
            "类目3": category_fields[2],
            "类目4": category_fields[3],
            "类目5": category_fields[4]
        }

    def generate_batch(self, count, platform=None):
        """批量生成账号"""
        return [self.generate_account(platform) for _ in range(count)]


# 注册自定义提供者
faker.add_provider(SocialMediaProvider)


def save_to_excel(accounts, filename="social_media_accounts1.xlsx"):
    """将账号数据保存到Excel文件，排除平台列"""
    if not accounts:
        print("没有数据可保存")
        return

    # 将数据转换为DataFrame
    df = pd.DataFrame(accounts)

    # 调整列顺序，排除平台列
    columns_order = [
        "账号", "性别", "邮箱", "国家", "内容", "个性化标签",
        "签约费用", "建联邮箱", "备注", "类目1", "类目2", "类目3", "类目4", "类目5"
    ]

    # 确保所有列都存在，按指定顺序排列
    for col in columns_order:
        if col not in df.columns:
            df[col] = ""

    df = df[columns_order]

    # 保存到Excel
    try:
        df.to_excel(filename, index=False)
        print(f"数据已成功保存到 {filename}")
    except Exception as e:
        print(f"保存文件时出错: {e}")


if __name__ == "__main__":
    # 示例：批量生成账号并保存到Excel
    print("\n" + "=" * 50)
    count = 50  # 生成50个账号
    print(f"批量生成{count}个账号并保存到Excel...")
    batch = faker.generate_batch(count)

    # 保存到Excel
    save_to_excel(batch, "social_media_accounts.xlsx")