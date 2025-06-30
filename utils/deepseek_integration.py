"""DeepSeek API集成工具"""
import os
import json
from openai import OpenAI

# 配置DeepSeek API
client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com/v1")

def get_fate_analysis(birth_date, birth_hour, gender, bone_weight, language="中文"):
    """获取DeepSeek的命理分析"""
    
    # 构造提示词
    prompt = f"""
    你是一位资深的中国命理学家，精通袁天罡称骨算命和铁板神数。
    请根据以下信息为用户提供详细的命理分析：
    
    - 出生日期: {birth_date}
    - 出生时辰: {birth_hour}
    - 性别: {gender}
    - 称骨重量: {bone_weight}两
    
    请用{language}回答，包含以下方面的分析：
    1. 婚姻状况
    2. 事业发展
    3. 健康状况
    4. 财富运势
    5. 人生建议
    
    分析应当:
    - 基于传统命理学原理
    - 结合现代生活实际
    - 给出建设性意见
    - 避免绝对化的负面预测
    - 强调人的主观能动性
    """
    
    # 调用DeepSeek API
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一位专业、友善的命理分析专家"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=2000
    )
    
    # 解析响应
    try:
        content = response.choices[0].message.content
        # 尝试解析为JSON (如果返回结构化数据)
        try:
            return json.loads(content)
        except:
            return {"analysis": content}
    except Exception as e:
        return {"error": str(e)}
