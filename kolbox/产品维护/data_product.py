import openpyxl
import random
import string

# 指定品牌名称和类目可选值
brand_names = ['modelones','Anker充电宝','CEMOY','Totwoo','资源储备']
categories = ['假发及配件','洗发/头发护理类产品','造型产品/工具/电器','身体彩绘','脸部化妆品','卸妆产品','儿童牙齿护理','口腔护理','牙刷及配件']

# 产品名称的词汇库
product_nouns = ["手机", "电脑", "耳机", "手表", "键盘", "鼠标", "平板", "相机"]
product_adjectives = ["智能", "高清", "无线", "超薄", "多功能", "专业", "便携"]

# 生成随机产品名称（从形容词和名词中组合）
def generate_product_name():
    adjective = random.choice(product_adjectives)
    noun = random.choice(product_nouns)
    return f"{adjective}{noun}"

# 生成随机型号（随机字母和数字组合）
def generate_model():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

# 生成随机链接（基于品牌名和产品名）
def generate_link():
    base = ''.join(random.choices(string.ascii_lowercase, k=5))
    return f"https://www.{base}.com/products/{random.randint(1000, 9999)}"

# 创建工作簿和工作表
workbook = openpyxl.Workbook()
sheet = workbook.active

# 设置表头
headers = ["产品名称", "品牌名称", "型号", "链接", "类目"]
sheet.append(headers)

# 生成并写入测试数据（默认50行，可通过命令行参数调整）
for _ in range(50):
    product_name = generate_product_name()
    brand = random.choice(brand_names)
    model = generate_model()
    link = generate_link()
    category = random.choice(categories)
    sheet.append([product_name, brand, model, link, category])

# 保存为新文件
workbook.save("产品维护_测试数据.xlsx")
print("测试数据生成并保存成功！")