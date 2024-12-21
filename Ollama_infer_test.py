from openai import OpenAI

client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='ollama',
)

def create_chinese_poetry(theme, style):
    creative_prompt = f"""你是一位精通中国古典诗词的文学大师。请基于以下要求创作：
    - 主题：{theme}
    - 风格：{style}
    - 要求：
        1. 创作一首符合格律的诗词
        2. 提供诗词的意境解析
        3. 给出每句的现代汉语解释
        4. 说明使用的意象和写作技巧
    
    请按以下格式输出：
    【诗词标题】
    【诗词内容】
    【意境解析】
    【现代解释】
    【写作技巧】
    """
    
    response = client.chat.completions.create(
        model="llama3.2",  # 或其他支持中文创作的模型
        messages=[
            {"role": "system", "content": "你是一位专业的古典诗词创作大师，精通诗词格律与意境营造。"},
            {"role": "user", "content": creative_prompt}
        ],
        temperature=0.8,  # 增加创造性
        max_tokens=1000
    )
    
    return response.choices[0].message.content

# 使用示例
themes = ["春天的江南", "塞外风光", "思乡之情", "月夜抒怀"]
styles = ["婉约", "豪放", "含蓄", "清新脱俗"]

# 创作不同主题和风格的诗词
for theme, style in zip(themes, styles):
    print(f"\n{'='*50}")
    print(f"创作主题：{theme}，风格：{style}")
    print(f"{'='*50}")
    poetry = create_chinese_poetry(theme, style)
    print(poetry)