import random
import string
import emoji

from faker import Faker
from faker.providers import BaseProvider

faker = Faker()
# faker = Faker('zh_CN') # 中文

email = faker.email()
username = faker.name()
country = faker.country()

# 自定义数据范围
class MyProvider(BaseProvider):
    # 国家
    def country(self):
        data = {
            "香港特别行政区": "HK", "中国": "CN", "美国": "US", "英国": "GB", "印度": "IN", "泰国": "TH", "日本": "JP",
            "阿联酋": "AE", "阿富汗": "AF", "阿尔巴尼亚": "AL", "亚美尼亚": "AM", "安哥拉": "AO", "阿根廷": "AR",
            "奥地利": "AT", "澳大利亚": "AU", "阿塞拜疆": "AZ", "孟加拉": "BD", "比利时": "BE", "布基纳法索": "BF",
            "保加利亚": "BG", "巴林": "BH", "布隆迪": "BI", "贝宁": "BJ", "巴勒斯坦": "BL", "文莱": "BN",
            "玻利维亚": "BO", "巴西": "BR", "博茨瓦纳": "BW", "白俄罗斯": "BY", "加拿大": "CA", "中非": "CF",
            "刚果": "CG", "瑞士": "CH", "智利": "CL", "喀麦隆": "CM", "哥伦比亚": "CO", "哥斯达黎加": "CR",
            "捷克": "CS", "古巴": "CU", "塞浦路斯": "CY", "德国": "DE", "丹麦": "DK", "多米尼加共和国": "DO",
            "阿尔及利亚": "DZ", "厄瓜多尔": "EC", "爱沙尼亚": "EE", "埃及": "EG", "西班牙": "ES", "埃塞俄比亚": "ET",
            "芬兰": "FI", "斐济": "FJ", "法国": "FR", "加蓬": "GA", "格林纳达": "GD", "格鲁吉亚": "GE", "加纳": "GH",
            "几内亚": "GN", "希腊": "GR", "危地马拉": "GT", "洪都拉斯": "HN", "匈牙利": "HU", "印度尼西亚": "ID",
            "爱尔兰": "IE", "以色列": "IL", "伊拉克": "IQ", "伊朗": "IR", "冰岛": "IS", "意大利": "IT", "牙买加": "JM",
            "约旦": "JO", "吉尔吉斯坦": "KG", "柬埔寨": "KH", "北朝鲜": "KP", "韩国": "KR", "科特迪瓦共和国": "KT",
            "科威特": "KW", "哈萨克": "KZ", "老挝": "LA", "黎巴嫩": "LB", "圣卢西亚": "LC", "列支敦士登": "LI",
            "斯里兰卡": "LK", "利比里亚": "LR", "立陶宛": "LT", "卢森堡": "LU", "拉脱维亚": "LV", "利比亚": "LY",
            "摩洛哥": "MA", "摩纳哥": "MC", "摩尔多瓦": "MD", "马达加斯加": "MG", "马里": "ML", "缅甸": "MM", "蒙古": "MN",
            "澳门地区": "MO", "马耳他": "MT", "毛里求斯": "MU", "马拉维": "MW", "墨西哥": "MX", "马来西亚": "MY",
            "莫桑比克": "MZ", "纳米比亚": "NA", "尼日尔": "NE", "尼日利亚": "NG", "尼加拉瓜": "NI", "荷兰": "NL",
            "挪威": "NO", "尼泊尔": "NP", "新西兰": "NZ", "阿曼": "OM", "巴拿马": "PA", "秘鲁": "PE", "巴布亚新几内亚": "PG",
            "菲律宾": "PH", "巴基斯坦": "PK", "波兰": "PL", "葡萄牙": "PT", "巴拉圭": "PY", "卡塔尔": "QA", "罗马尼亚": "RO",
            "俄罗斯": "RU", "沙特阿拉伯": "SA", "塞舌尔": "SC", "苏丹": "SD", "瑞典": "SE", "新加坡": "SG", "斯洛文尼亚": "SI",
            "斯洛伐克": "SK", "圣马力诺": "SM", "塞内加尔": "SN", "索马里": "SO", "叙利亚": "SY", "斯威士兰": "SZ", "乍得": "TD",
            "多哥": "TG", "塔吉克斯坦": "TJ", "土库曼": "TM", "突尼斯": "TN", "土耳其": "TR", "台湾省": "TW", "坦桑尼亚": "TZ",
            "乌克兰": "UA", "乌干达": "UG", "乌拉圭": "UY", "乌兹别克": "UZ", "圣文森特岛": "VC", "委内瑞拉": "VE", "越南": "VN",
            "也门": "YE", "南斯拉夫联盟": "YU", "南非": "ZA", "赞比亚": "ZM", "扎伊尔": "ZR", "津巴布韦": "ZW"
        }
        return random.choice(list(data.keys()))
    # 性别
    def gender(self):
        return random.choice(['男','女'])

    # 平台
    def platform(self):
        return random.choice(["IG", "YT", "TK"])


    # 内容
    # 使用方式：传入平台类型，返回该类型全部内容（content = faker.content("YT")）
    def content(self, account_type=None):
        content_options = {
            "IG": ["IG Reel", "IG Story", "IG Post"],
            "YT": ["YT专题5-10min", "YT插播2-3min"],
            "TK": ["TikTok视频", "TK直播"]
        }
        # 如果未传入账号类型，则随机选择一个
        if account_type is None:
            selected_account = self.account()
        else:
            selected_account = account_type
        # 返回指定账号下的所有内容选项
        return content_options.get(selected_account, [])


    # 标签类型
    def label_type(self):
        return random.choice(["标签", "关键词", "种子视频", "种子账号", "关注列表"])

    # 标签
    def label(self):
        return random.choice(["hometip", "decoration", "setupreview", "hacks"])

    # 品牌
    def brand(self):
        return random.choice(["eufy", "Miniso"])

    # 类目
    def category(self):
        return random.choices(["护肤","彩妆"])



    # -------------------------------------

    def generate_tiktok_username(self):
        allowed_chars = string.ascii_letters + string.digits + '_.'
        length = random.randint(2, 24)

        if length >= 4:
            username = [
                random.choice(string.ascii_letters),
                random.choice(string.digits),
                random.choice('_.'),
            ]
            username.extend(random.choice(allowed_chars) for _ in range(length - 3))
            random.shuffle(username)
            username = ''.join(username)
        else:
            username = ''.join(random.choice(allowed_chars) for _ in range(length))

        if username.endswith('.') and len(username) > 1:
            username = username[:-1] + random.choice(allowed_chars.replace('.', ''))
        return username

    def generate_youtube_username(self,include_emoji=False):
        length = random.randint(1, 60)
        base_chars = string.ascii_letters + string.digits + '!@#$%^&*()_+-=[]{}|;:\'",.<>/? '

        emoji_ranges = [
            (0x1F600, 0x1F64F),
            (0x1F300, 0x1F5FF),
            (0x1F900, 0x1F9FF),
        ]

        def get_random_emoji():
            range_idx = random.randint(0, len(emoji_ranges) - 1)
            char_code = random.randint(emoji_ranges[range_idx][0], emoji_ranges[range_idx][1])
            return chr(char_code)

        username = []
        for _ in range(length):
            if include_emoji and random.random() < 0.2:
                username.append(get_random_emoji())
            else:
                username.append(random.choice(base_chars))

        return ''.join(username)

    def generate_instagram_username(self):
        length = random.randint(3, 30)
        first_chars = string.ascii_letters + '_'
        allowed_chars = string.ascii_letters + string.digits + '_.'

        first_char = random.choice(first_chars)

        if length >= 4:
            middle_chars = [random.choice(allowed_chars) for _ in range(length - 2)]
            if '.' in allowed_chars and length > 4 and random.random() > 0.5:
                pos = random.randint(1, len(middle_chars) - 1)
                middle_chars[pos] = '.'
        else:
            middle_chars = [random.choice(allowed_chars.replace('.', '')) for _ in range(length - 2)]

        last_char = random.choice(allowed_chars.replace('.', ''))

        return first_char + ''.join(middle_chars) + last_char

    def generate_youtube_usernames(self,count):
        if count < 1:
            return []
        # 确保有且仅有一个带emoji
        usernames = [count.generate_youtube_username(include_emoji=True)]
        usernames.extend(self.generate_youtube_username(include_emoji=False) for _ in range(count - 1))
        random.shuffle(usernames)
        return usernames

    # -----------------------------------------

    def account(self):
        platform = random.choices(["IG", "YT", "TK"], weights=[20, 40, 40], k=1)[0]

        if platform == "TK":
            return self.generate_tiktok_username()
        elif platform == "IG":
            return self.generate_instagram_username()
        elif platform == "YT":
            return self.generate_youtube_usernames(5)
        else:
            return "Unknown"


# 添加到Faker实例
faker.add_provider(MyProvider)

# 使用自定义提供者
if __name__ == "__main__":

    username = faker.account()
    print(username)

