"""阳历转阴历转换工具"""
import datetime
from zhdate import ZhDate

def solar_to_lunar(year, month, day):
    """将阳历日期转换为阴历日期"""
    lunar_date = ZhDate.from_datetime(datetime.datetime(year, month, day))
    lunar_month_cn = lunar_date.lunar_month_cn  # e.g., "闰二月" or "二月"
    is_leap = lunar_month_cn.startswith("闰")
    leap_prefix = "闰" if is_leap else ""
    return (
        lunar_date.lunar_year,
        leap_prefix + str(lunar_date.lunar_month),
        lunar_date.lunar_day
    )




