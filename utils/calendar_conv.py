"""阳历转阴历转换工具"""
"""阳历转阴历转换工具"""
import datetime
from zhdate import ZhDate

def solar_to_lunar(year, month, day):
    """将阳历日期转换为阴历日期"""
    lunar_date = ZhDate.from_datetime(datetime.datetime(year, month, day))
    
    # For zhdate==0.1 compatibility
    lunar_month_str = lunar_date.chinese().split('年')[1].split('月')[0]
    is_leap = '闰' in lunar_month_str
    
    return (
        lunar_date.lunar_year,
        lunar_date.lunar_month,
        lunar_date.lunar_day,
        "闰" if is_leap else ""
    )


