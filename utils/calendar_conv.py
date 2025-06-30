"""阳历转阴历转换工具"""
import datetime
from zhdate import ZhDate

def solar_to_lunar(year, month, day):
    """将阳历日期转换为阴历日期"""
    lunar_date = ZhDate.from_datetime(datetime.datetime(year, month, day))

    # 获取中文月份字符串，例如："闰二月" 或 "二月"
    lunar_month_cn = lunar_date.lunar_month_cn
    is_leap = lunar_month_cn.startswith("闰")
    lunar_month_num = lunar_date.lunar_month  # 是数字 1-12

    # 决定是否加“闰”字
    leap_prefix = "闰" if is_leap else ""

    return (
        lunar_date.lunar_year,
        leap_prefix + str(lunar_month_num),
        lunar_date.lunar_day
    )



