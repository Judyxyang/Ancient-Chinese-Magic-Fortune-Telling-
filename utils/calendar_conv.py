"""阳历转阴历转换工具"""
import datetime
from zhdate import ZhDate

def solar_to_lunar(year, month, day):
    """将阳历日期转换为阴历日期"""
    lunar_date = ZhDate.from_datetime(datetime.datetime(year, month, day))
    
    leap_prefix = "闰" if lunar_date.is_leap_month else ""
    
    return (
        lunar_date.lunar_year,
        leap_prefix + str(lunar_date.lunar_month),
        lunar_date.lunar_day
    )

