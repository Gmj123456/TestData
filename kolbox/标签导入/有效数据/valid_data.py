import pandas as pd
import random
import string

# 固定值定义
brands = ["eufy", "Miniso", "patpat婴儿车"]
categories = ["医美器材", "OOTD"]

# 构建平台与标签类型对应关系及输出文件名
platform_config = {
    "TK": {
        "name": "Tiktok",
        "tag_types": ["标签"],
        "output_file": "tiktok_test_data.xlsx",
        "tag_allow_space": False  # Tk平台标签不允许空格
    },
    "YT": {
        "name": "Youtube",
        "tag_types": ["标签", "种子视频", "关键词"],
        "output_file": "youtube_test_data.xlsx",
        "tag_allow_space": True  # YT平台标签允许空格
    },
    "IG": {
        "name": "Instagram",
        "tag_types": ["标签", "种子账号", "关注列表"],
        "output_file": "instagram_test_data.xlsx",
        "tag_allow_space": True  # IG平台标签允许空格
    }
}


# 生成随机字符串（用于标签、适合产品、受众人群等字段）
def generate_random_str(length=10, allow_space=False):
    if allow_space:
        # 允许空格的字符集
        chars = string.ascii_letters + string.digits + "_." + " "
        # 确保字符串不以空格开头或结尾
        result = random.choice(string.ascii_letters + string.digits)
        result += "".join(random.choice(chars) for _ in range(length - 2))
        result += random.choice(string.ascii_letters + string.digits)
        return result
    else:
        # 不允许空格的字符集
        chars = string.ascii_letters + string.digits + "_."
        return "".join(random.choice(chars) for _ in range(length))


# 生成指定平台的测试数据
def generate_test_data(platform_info, count=10):
    data = []
    for _ in range(count):
        tag_type = random.choice(platform_info["tag_types"])

        sort_val = random.randint(1, 100) if random.random() < 0.8 else None
        # 根据平台配置决定标签是否允许空格
        tag = generate_random_str(15, platform_info.get("tag_allow_space", False))
        brand = random.choice(brands)
        suitable_product = generate_random_str(15, allow_space=True)
        audience = generate_random_str(15, allow_space=True)
        category = random.choice(categories)
        video_link = ""
        force_update_status = ""

        data.append([
            sort_val, tag, brand, suitable_product,
            audience, category, tag_type, video_link,
            force_update_status
        ])

    return data


def main():
    # 为每个平台生成测试数据并保存到对应的Excel文件
    for platform_code, platform_info in platform_config.items():
        try:
            # 生成测试数据
            data = generate_test_data(platform_info, count=10)

            # 创建DataFrame
            columns = ["排序", "标签", "品牌", "适合产品", "受众人群", "类目", "标签类型", "视频链接",
                       "强制更新标签状态"]
            df = pd.DataFrame(data, columns=columns)

            # 保存到Excel
            df.to_excel(platform_info["output_file"], index=False)
            print(
                f"已成功为 {platform_info['name']}({platform_code}) 生成并保存 {len(data)} 条测试数据到 {platform_info['output_file']}")

        except Exception as e:
            print(f"为 {platform_info['name']} 生成数据时出错: {str(e)}")


if __name__ == "__main__":
    main()