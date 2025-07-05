import google.generativeai as genai
import os
from datetime import datetime

# 确保您已经配置了 Gemini API Key
genai.configure(api_key="YOUR_GEMINI_API_KEY") # 请替换为您的实际API Key

# 初始化模型
model = genai.GenerativeModel('gemini-pro')

# Step 1: 定义 Google Search 工具函数
# 这个函数将由模型调用，并期望您在内部实现真实的搜索逻辑
@genai.tool
def Google_Search(query: str) -> str:
    """
    通过 Google 搜索获取信息。
    此工具用于查询互联网，获取特定主题、实体或事件的最新和相关信息。
    参数:
    query (str): 要执行的搜索查询字符串。
    """
    print(f"\n--- 模型正在请求 Google 搜索，查询内容: '{query}' ---")
    #
    # IMPORTANT: 在这里，您需要集成一个真实的 Google 搜索 API！
    # 以下是一个模拟的实现，因为它无法真正执行搜索。
    # 您可以考虑使用：
    # - Google Custom Search API (需要配置和API Key)
    # - SerpApi (一个第三方服务，封装了多种搜索引擎，需要API Key)
    # - 其他您能访问的搜索服务
    #
    # 示例 (使用 SerpApi 的伪代码，您需要安装 serpapi 库并替换 YOUR_SERPAPI_API_KEY):
    # from serpapi import GoogleSearch
    # params = {
    #     "q": query,
    #     "api_key": "YOUR_SERPAPI_API_KEY"
    # }
    # try:
    #     search = GoogleSearch(params)
    #     results = search.get_dict()
    #     organic_results = results.get("organic_results", [])
    #     search_summary = ""
    #     for i, res in enumerate(organic_results[:3]): # 只取前3条结果的摘要
    #         search_summary += f"标题: {res.get('title')}\n链接: {res.get('link')}\n摘要: {res.get('snippet')}\n\n"
    #     if not search_summary:
    #         return "未找到相关搜索结果。"
    #     return search_summary
    # except Exception as e:
    #     return f"搜索工具调用失败: {e}"

    # 临时模拟返回一个结果，以便代码能够运行
    if "TikTok账号@.hypey" in query or "TikTok @.hypey" in query:
        return "模拟搜索结果：TikTok账号@.hypey 主要内容为潮流穿搭、美妆分享和日常生活Vlog。其视频形式多变，包含OOTD展示、产品开箱测评。该账号与多个时尚和美妆品牌有合作，评论区互动活跃，粉丝画像偏向年轻女性。更新频率较高，每周发布多条视频。"
    elif "Charli D'Amelio TikTok" in query:
        return "模拟搜索结果：Charli D'Amelio 是TikTok上知名的舞者和内容创作者，以其病毒式舞蹈视频和对口型内容而闻名。她有大量品牌合作，如Dunkin' Donuts和Morphe。主要受众是青少年。"
    else:
        return f"模拟搜索结果：关于 '{query}' 的通用信息，模型无法直接访问网页内容。"

# Step 2: 调用 generate_content 时，将工具列表传递给模型
prompt_text = """
# 社交媒体达人类型分析指令

## 角色设定
你是一名资深社交媒体分析师，擅长通过内容特征、商业行为和用户互动数据精准定位达人类型。请根据提供的TikTok账号链接进行多维度分析。

## 输入数据
- 目标账号:https://www.tiktok.com/@.hypey
- 分析要求: 必须匹配到二级类目

## 分类体系
### 一级类目 → 二级类目（关键特征）
### 1. 科技评测类  
- 消费电子数码类  
- 智能家居生态类  
- 数码配件极客类  
- 摄影影像器材类  
- 前沿科技体验类  
- 软件与AI工具类  
- 电竞外设硬核类  
- 汽车科技出行类  
- 健康科技穿戴类  
- 环保科技可持续类  
### 2. 开箱测评类  
- 消费电子快消开箱  
- 美妆个护惊喜开箱  
- 家居生活实用开箱  
- 服饰穿搭惊喜开箱  
- 潮玩盲盒沉浸开箱  
- 食品饮品感官开箱  
- 母婴育儿刚需开箱  
- 户外探险硬核开箱  
- 跨境小众猎奇开箱  
- 可持续环保开箱  
### 3. 时尚穿搭类  
- OOTD每日穿搭模板  
- 大码自信穿搭指南  
- 时尚配饰点睛术  
- 运动休闲混搭风  
- 职场通勤战袍库  
### 4. 美妆个护类  
- 彩妆教程  
- 护肤品成分测评  
- 美发造型技巧  
- 平价/大牌产品种草  
### 5. 家居生活类  
- 家居改造焕新  
- 智能家居体验  
- 收纳整理技巧  
- 家居DIY手作  
- 家居好物种草  
- 清洁技巧指南  
- 家居氛围美学  
- 家具深度评测  
### 6. 母婴亲子类  
- 母婴好物推荐清单  
- 家庭纪实Vlog  
- 亲子互动游戏库  
### 7. 健身运动类  
- 家庭健身指南  
- 健身教学全解析  
- 运动装备推荐库  
- 户外极限挑战  
- 小众文化运动  
### 8. 旅行探店类  
- 线下探店  
- 街头采访  
- 离网生活  
- 旅行Vlog与人文纪实  
- 景点攻略  
### 9. 美食烹饪类  
- 厨房工具推荐  
- 食谱教学  
- 美食探店  
### 10. 宠物萌宠类  
- 萌宠日常Vlog  
- 宠物用品好物推荐  
- 宠物行为训练所  
- 科学养宠指南  
### 11. 游戏电竞二次元类  
- 电竞赛事与战队解析  
- 二次元IP深度漫游  
- 硬核攻略实验室  
- 虚拟偶像与元宇宙  
- 外设与黑科技评测  
### 12. 泛娱乐内容创作类  
- 互动挑战赛工厂  
- 热舞擦边引力场  
- 明星二创与热梗工场  
- 搞笑短剧工坊  
### 13. 汽车出行类  
- 汽车评测（新能源车/改装车）  
- 车载好物推荐  
### 14. 文化手作类  
- 手工DIY创意工坊  
- 书法绘画艺术研习  
- 非遗文化传承实践  
### 15. 知识教育  
- 学科知识精讲  
- 实用技能工坊  
- 教育认知与心理  

## 分析框架
|||
|---|---|
|**内容维度**|• 主题集中度（TOP3内容标签）• 视频形式（口播/剧情/Vlog等）• 更新频率|
|**商业维度**|• 带货链接密度 • 品牌合作类型 • 广告植入方式|
|**用户维度**|• 评论区高频词分析 • 粉丝画像特征（年龄/性别/地域）|

## 输出要求
```json
{
  "达人类型": {
    "一级类目": "时尚穿搭类",
    "二级类目": "OOTD每日穿搭模板",
    "匹配度": "高（80%内容符合）"
  },
  "分析依据": [
    {
      "维度": "内容特征",
      "证据": "近30条视频中24条为每日穿搭展示，使用#ootd标签"
    },
    {
      "维度": "商业特征",
      "证据": "与Nike、H&M等服装品牌有固定合作"
    }
  ],
  "存疑指标": ["偶尔发布舞蹈内容（需排除泛娱乐类）"]
}   
"""

response = model.generate_content(
    contents=prompt_text,
    tools=[Google_Search] # 将您定义的工具列表传递给模型
)

# Step 3: 处理模型的响应
# 模型可能会直接给出答案，或者建议调用工具，或者生成工具调用
# 如果 response.candidates[0].content.parts 包含 function_call，说明模型想要调用工具
try:
    print("\n--- 模型原始响应 ---")
    print(response.text) # 尝试直接打印文本响应

    # 检查模型是否决定调用工具
    if response.candidates and response.candidates[0].content.parts:
        for part in response.candidates[0].content.parts:
            if part.function_call:
                function_call = part.function_call
                print(f"\n--- 模型决定调用工具: {function_call.name} ---")
                print(f"参数: {function_call.args}")

                # 实际执行工具调用
                tool_output = None
                if function_call.name == "Google Search":
                    # 在这里调用您定义的 Google Search 函数
                    tool_output = Google_Search(query=function_call.args["query"])
                    print(f"\n--- 工具返回结果: {tool_output} ---")

                # 将工具的输出发送回模型，以便模型基于此生成最终回答
                if tool_output:
                    follow_up_response = model.generate_content(
                        contents=[prompt_text, part, {"text": tool_output}]
                    )
                    print("\n--- 模型基于工具结果的最终回答 ---")
                    print(follow_up_response.text)
                    final_response_text = follow_up_response.text
                else:
                    final_response_text = response.text # 如果没有工具输出，用原始响应
            else:
                final_response_text = response.text # 如果模型没有调用工具，用原始响应

except Exception as e:
    print(f"\n处理模型响应时发生错误: {e}")
    final_response_text = "抱歉，生成响应时出现问题或模型未能完成分析。"


# 保存到txt文件（带时间戳）
output_dir = "D:/gmj/workSpaces/workSpaces_pycharm/data_kolbox/gemini/demo_prompt/output" # 使用绝对路径或确保目录存在
os.makedirs(output_dir, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = os.path.join(output_dir, f"gemini_output_{timestamp}.txt")

with open(output_file, "w", encoding="utf-8") as f:
    f.write(final_response_text)

print(f"\n结果已保存到: {output_file}")