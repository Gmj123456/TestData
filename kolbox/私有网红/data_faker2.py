import random
import string
from faker import Faker
from faker.providers import BaseProvider
import pandas as pd  # 用于导出Excel

from get_mysql_data.get_mysql_data_kolbox import DataRepository

# 初始化Faker
faker = Faker()

# 创建存储库实例
repo = DataRepository()


class SocialMediaProvider(BaseProvider):
    """私有网红账号生成器，符合各平台规则"""
    # 从数据库已有固定值中随机选取：国家、品牌、建联邮箱、类目
    def country(self):
        """随机选择国家"""
        country_list = repo.fetch_countries()
        return random.choice(country_list)

    def brand(self):
        """随机选择品牌"""
        brand_list = repo.fetch_brands()
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

    # 定义标签类型及其对应的标签列表
    TAG_CATEGORIES = {
        "职业": ["艺术家", "编辑", "训狗师", "医生", "演说家", "发型师", "心理师", "电视主持人", "房产中介", "乐队歌手",
                 "小明星", "教程创作者"],
        "兴趣爱好": ["打猎", "游泳", "瑜伽", "吉他", "编织", "游戏", "咖啡", "美食", "穿搭", "美妆", "护肤", "园艺",
                     "DIY"],
        "产品类型": ["eufy摄像头", "wlwe收纳柜", "ekouaer女士睡衣", "假发", "miniso名创", "rainpoint花园浇灌",
                     "diy工具", "dreame洗地机", "inia脱毛仪", "trihill音箱"],
        "生活方式": ["亚裔", "同性恋", "跨性别", "双胞胎", "单亲家庭", "基督教", "living alone", "极简主义",
                     "可持续生活"],
        "内容形式": ["搞笑/抽象", "生活分享", "情感分享", "视频剪辑", "经验干货", "街头采访", "开箱测评", "装修日记"],
        "场景": ["圣诞节", "居家办公", "户外冒险", "职场生活", "校园生活", "旅行", "美食制作", "宠物日常"]
    }

    def label(self, TAG_CATEGORIES=TAG_CATEGORIES):
        """从不同类型中随机生成标签"""
        # 随机选择标签类型
        if TAG_CATEGORIES is None:
            TAG_CATEGORIES = TAG_CATEGORIES
        category = random.choice(list(TAG_CATEGORIES.keys()))
        # 从选中的类型中随机选择标签
        return random.choice(TAG_CATEGORIES[category])

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

    def jianlian_email(self, advisor_name: str):
        """
        根据指定顾问名获取建联邮箱，若未指定则抛出异常

        Args:
            advisor_name: 顾问用户名（必需）

        Returns:
            对应的建联邮箱地址

        Raises:
            ValueError: 未提供顾问名或未找到邮箱记录
        """
        if not advisor_name:
            raise ValueError("必须指定顾问名(advisor_name)才能获取建联邮箱")

        # 根据用户名获取邮箱列表
        emails = repo.fetch_contact_email(advisor_name)
        if not emails:
            raise ValueError(f"未找到顾问 '{advisor_name}' 的邮箱记录")

        return random.choice(emails)

    def generate_account(self, platform=None, advisor_name: str = None):
        """生成单个账号，必须指定顾问名"""
        if not advisor_name:
            raise ValueError("generate_account方法必须指定advisor_name参数")

        if not platform:
            platform = self.platform()

        platform_names = {"TK": "TikTok", "IG": "Instagram", "YT": "YouTube"}
        platform_name = platform_names.get(platform, "未知平台")

        if platform == "TK":
            username = self.generate_tiktok_username()
        elif platform == "IG":
            username = self.generate_instagram_username()
        elif platform == "YT":
            username = self.generate_youtube_username()
        else:
            username = "invalid_user"

        email = self.generate_email()
        jianlian_email = self.jianlian_email(advisor_name)
        signing_fee = round(random.uniform(1000, 10000), 2)
        note = self.generate_random_note()

        # 获取类目选项
        category_options = repo.fetch_category()

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

    def generate_batch(self, count, advisor_name: str, platform=None):
        """批量生成账号，必须指定顾问名"""
        return [self.generate_account(platform, advisor_name) for _ in range(count)]


# 注册自定义提供者
faker.add_provider(SocialMediaProvider)


def save_to_excel(accounts, filename="social_media_accounts.xlsx"):
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

    # 在文件名中添加时间戳
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    # 修改文件名格式，在基本名和扩展名之间插入时间戳
    base_name, ext = filename.rsplit('.', 1)
    timestamped_filename = f"{base_name}_{timestamp}.{ext}"

    # 保存到Excel
    try:
        df.to_excel(timestamped_filename, index=False)
        print(f"数据已成功保存到 {timestamped_filename}")
    except Exception as e:
        print(f"保存文件时出错: {e}")


if __name__ == "__main__":
    # 示例：批量生成账号并保存到Excel
    print("\n" + "=" * 50)
    count = 50  # 生成50个账号
    advisor = "gw1 "  # 必须指定顾问名
    print(f"批量生成{count}个账号并保存到Excel...")
    batch = faker.generate_batch(count, advisor)

    # 保存到Excel
    save_to_excel(batch, "social_media_accounts.xlsx")