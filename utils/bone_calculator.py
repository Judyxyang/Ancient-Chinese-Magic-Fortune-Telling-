"""袁天罡称骨算命计算逻辑"""

# 年重量对照表（两）
YEAR_WEIGHTS = {
    1924: 0.8, 1925: 0.8, 1926: 0.6, 1927: 0.7, 1928: 0.8,
    # 完整数据需要补充...
    2020: 0.7, 2021: 0.7, 2022: 0.8, 2023: 0.8
}

# 月重量对照表（两）
MONTH_WEIGHTS = {
    1: 0.6, 2: 0.7, 3: 1.8, 4: 0.9, 5: 0.5,
    6: 1.6, 7: 0.9, 8: 1.5, 9: 1.8, 10: 0.8,
    11: 0.9, 12: 0.5
}

# 日重量对照表（两）
DAY_WEIGHTS = {
    1: 0.5, 2: 1.0, 3: 0.8, 4: 1.5, 5: 1.6,
    # 完整数据需要补充...
    30: 0.9, 31: 1.0
}

# 时辰重量对照表（两）
HOUR_WEIGHTS = {
    0: 1.6, 1: 0.6, 2: 0.6, 3: 0.7, 4: 1.0,
    5: 1.0, 6: 0.9, 7: 0.9, 8: 1.6, 9: 0.6,
    10: 0.6, 11: 0.7
}

def calculate_bone_weight(lunar_date, hour_code, gender_code):
    """计算称骨重量"""
    year, month, day, _ = lunar_date
    
    # 计算各部分重量
    year_weight = YEAR_WEIGHTS.get(year, 0.0)
    month_weight = MONTH_WEIGHTS.get(month, 0.0)
    day_weight = DAY_WEIGHTS.get(day, 0.0)
    hour_weight = HOUR_WEIGHTS.get(hour_code, 0.0)
    
    # 性别修正
    gender_weight = 0.0
    if gender_code == 0:  # 男
        gender_weight = 0.1
    else:  # 女
        gender_weight = -0.1
    
    total_weight = round(year_weight + month_weight + day_weight + hour_weight + gender_weight, 1)
    
    # 返回详细计算过程
    breakdown = [
        {"item": "年份", "weight": year_weight},
        {"item": "月份", "weight": month_weight},
        {"item": "日期", "weight": day_weight},
        {"item": "时辰", "weight": hour_weight},
        {"item": "性别", "weight": gender_weight}
    ]
    
    return total_weight, breakdown
