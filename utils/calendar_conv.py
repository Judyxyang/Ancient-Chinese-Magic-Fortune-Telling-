"""阳历转阴历转换工具（兼容zhdate==0.1）"""
import datetime
from zhdate import ZhDate

def solar_to_lunar(year, month, day):
    """将阳历日期转换为阴历日期（适配Streamlit Cloud）"""
    lunar_date = ZhDate.from_datetime(datetime.datetime(year, month, day))
    
    # zhdate 0.1兼容方案
    date_str = lunar_date.chinese()  # 示例："二零二三年闰二月十五"
    is_leap = "闰" in date_str
    
    return (
        lunar_date.lunar_year,
        lunar_date.lunar_month,
        lunar_date.lunar_day,
        "闰" if is_leap else ""
    )



