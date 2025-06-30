import os
# from openai import OpenAI  # ← Remove this
from deepseek import DeepSeek  # ← Use this
from config import DEEPSEEK_API_KEY, DEEPSEEK_MODEL

client = OpenAI(api_key=DEEPSEEK_API_KEY)

def get_simple_analysis(birth_date, birth_hour, gender, bone_weight, language="中文"):
    """获取基础版AI分析"""
    prompt = f"""
    作为命理专家，请根据以下信息提供简洁分析:
    - 出生日期: {birth_date}
    - 出生时辰: {birth_hour}
    - 性别: {gender}
    - 称骨重量: {bone_weight}两
    
    要求:
    - 使用{language}回答
    - 200字以内
    - 包含运势总评
    - 给出1条改进建议
    - 语气积极正面
    """
    
    response = client.chat.completions.create(
        model=DEEPSEEK_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=500
    )
    
    return response.choices[0].message.content

def get_premium_analysis(birth_date, birth_time, gender, bone_weight, birth_place="", current_city="", language="中文"):
    """获取高级版AI分析"""
    prompt = f"""
    作为资深命理专家，请提供全面分析:
    
    ## 基本信息
    - 出生日期: {birth_date}
    - 出生时间: {birth_time}
    - 性别: {gender}
    - 称骨重量: {bone_weight}两
    - 出生地: {birth_place or "未提供"}
    - 现居地: {current_city or "未提供"}
    
    ## 分析要求
    使用{language}回答，包含以下部分:
    1. 总体运势(overview): 200字总结
    2. 婚姻感情(marriage): 分析婚姻状况，给出婚姻指数(0-100)和最佳婚期
    3. 事业财富(career): 分析事业发展，列出3-5个适合职业
    4. 健康养生(health): 分析健康状况，给出养生建议
    5. 流年运势(yearly_luck): 分析未来10年运势
    6. 其他建议(advice): 3条具体建议
    
    ## 格式要求
    返回JSON格式，包含以上所有字段
    """
    
    response = client.chat.completions.create(
        model=DEEPSEEK_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        response_format={"type": "json_object"},
        max_tokens=2000
    )
    
    try:
        import json
        return json.loads(response.choices[0].message.content)
    except:
        return {"error": "分析生成失败"}
