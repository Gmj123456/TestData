import pandas as pd
import random
import string

# 固定值定义
brands = ["eufy", "Miniso", "patpat婴儿车", "invalid_brand"]
categories = ["医美器材", "OOTD", "invalid_category"]
force_update_options = ["是", "否", "", "yes", "no", "123", "invalid"]

# 所有可能的标签类型
ALL_TAG_TYPES = ["标签", "种子视频", "关键词", "种子账号", "关注列表", "invalid_tag_type"]

# 构建平台与标签类型对应关系及输出文件名
platform_config = {
    "TK": {
        "name": "Tiktok",
        "valid_tag_types": ["标签"],
        "output_file": "tiktok_invalid_test_data.xlsx"
    },
    "YT": {
        "name": "Youtube",
        "valid_tag_types": ["标签", "种子视频", "关键词"],
        "output_file": "youtube_invalid_test_data.xlsx"
    },
    "IG": {
        "name": "Instagram",
        "valid_tag_types": ["标签", "种子账号", "关注列表"],
        "output_file": "instagram_invalid_test_data.xlsx"
    }
}


# 生成随机字符串
def generate_random_str(length=10, invalid_chars="", allow_space=False):
    if allow_space:
        chars = string.ascii_letters + string.digits + "_." + " " + invalid_chars
    else:
        chars = string.ascii_letters + string.digits + "_." + invalid_chars

    result = ''.join(random.choice(chars) for _ in range(length))

    # 确保至少包含一个无效字符（如果提供了无效字符）
    if invalid_chars and not any(c in invalid_chars for c in result):
        pos = random.randint(0, length - 1)
        result = result[:pos] + random.choice(invalid_chars) + result[pos + 1:]

    return result


# 生成随机视频ID
def generate_video_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=11))


# 生成无效排序值
def generate_invalid_sort():
    options = [
        random.randint(-100, 0),  # 负数或零
        random.choice(["", "abc", "123a", "1 2 3"]),  # 空值、非数字
        999999999999,  # 超大数字
        0.5  # 小数
    ]
    return random.choice(options)


# 生成无效标签
def generate_invalid_tag(tag_type):
    # 标签类型为"标签"时，必须生成包含空格或非法字符的标签
    if tag_type == "标签":
        invalid_chars = "!@#$%^&*()<>[]{}/\\|"
        return generate_random_str(15, invalid_chars, allow_space=True)

    # 其他标签类型生成超长或其他非法格式
    if random.random() < 0.5:
        return "a" * 51  # 超长标签
    else:
        return generate_random_str(15, invalid_chars="!@#$%^&*()")


# 生成无效视频链接
def generate_invalid_video_link():
    options = [
        "",  # 空链接
        "invalid_url",  # 无效URL
        "http://invalid.com",  # 非平台特定URL
        f"https://www.randomsite.com/watch?v={generate_video_id()}",  # 错误平台
        "https://youtube.com",  # 缺少视频ID
        "https://youtube.com/v=invalid"  # 错误格式
    ]
    return random.choice(options)


# 生成无效强制更新状态
def generate_invalid_force_update():
    invalid_options = [o for o in force_update_options if o not in ["是", "否", ""]]
    return random.choice(invalid_options)


# 生成指定平台的测试数据
def generate_test_data(platform_info, count=20):
    data = []
    valid_tags = platform_info["valid_tag_types"]
    invalid_tags = [t for t in ALL_TAG_TYPES if t not in valid_tags]

    for _ in range(count):
        # 随机决定错误类型
        error_type = random.randint(1, 8)  # 8种错误类型

        # 基础数据
        if error_type == 1:
            # 1. 平台与标签类型不匹配
            tag_type = random.choice(invalid_tags)
        else:
            tag_type = random.choice(valid_tags)

        # 2. 无效排序值
        if error_type == 2:
            sort_val = generate_invalid_sort()
        else:
            sort_val = random.randint(1, 100) if random.random() < 0.8 else None

        # 3. 无效标签
        if error_type == 3 or (tag_type == "标签" and error_type != 1):
            tag = generate_invalid_tag(tag_type)
        else:
            allow_space_in_tag = tag_type != "标签"
            tag = generate_random_str(15, allow_space=allow_space_in_tag)

        # 4. 无效品牌
        if error_type == 4:
            brand = "invalid_brand"
        else:
            brand = random.choice(brands[:-1])

        # 5. 无效适合产品
        if error_type == 5:
            suitable_product = generate_random_str(15, invalid_chars="<>[]{}/\\|", allow_space=True)
        else:
            suitable_product = generate_random_str(15, allow_space=True)

        # 6. 无效受众人群
        if error_type == 6:
            audience = generate_random_str(15, invalid_chars="<>[]{}/\\|", allow_space=True)
        else:
            audience = generate_random_str(15, allow_space=True)

        # 7. 无效类目
        if error_type == 7:
            category = "invalid_category"
        else:
            category = random.choice(categories[:-1])

        # 8. 无效视频链接
        if tag_type == "种子视频":
            if error_type == 8 or random.random() < 0.5:  # 50%概率生成无效链接
                video_link = generate_invalid_video_link()
            else:
                platform_domain = {
                    "TK": "tiktok.com",
                    "YT": "youtube.com",
                    "IG": "instagram.com"
                }
                domain = platform_domain.get(platform_info["name"][:2], "example.com")
                video_link = f"https://www.{domain}/watch?v={generate_video_id()}"
        else:
            # 非种子视频类型，20%概率生成非空链接
            if random.random() < 0.2:
                video_link = f"https://www.randomsite.com/watch?v={generate_video_id()}"
            else:
                video_link = ""

        # 9. 无效强制更新状态（20%概率）
        if random.random() < 0.2:
            force_update_status = generate_invalid_force_update()
        else:
            force_update_status = random.choice(["是", "否", ""])

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
            data = generate_test_data(platform_info, count=50)  # 每个平台生成50条测试数据

            # 创建DataFrame
            columns = ["排序", "标签", "品牌", "适合产品", "受众人群", "类目", "标签类型", "视频链接",
                       "强制更新标签状态"]
            df = pd.DataFrame(data, columns=columns)

            # 保存到Excel
            df.to_excel(platform_info["output_file"], index=False)
            print(
                f"已成功为 {platform_info['name']}({platform_code}) 生成并保存 {len(data)} 条无效测试数据到 {platform_info['output_file']}")

        except Exception as e:
            print(f"为 {platform_info['name']} 生成无效数据时出错: {str(e)}")


if __name__ == "__main__":
    main()