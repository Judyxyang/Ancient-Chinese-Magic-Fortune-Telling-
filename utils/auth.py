import streamlit as st
from config import PREMIUM_PRICE

def solar_to_lunar(year, month, day):
    """将阳历日期转换为阴历日期"""
    from zhdate import ZhDate
    import datetime

    lunar_date = ZhDate.from_datetime(datetime.datetime(year, month, day))
    
    leap_prefix = "闰" if lunar_date.lunar_month_cn.startswith("闰") else ""
    
    return (
        lunar_date.lunar_year,
        leap_prefix + str(lunar_date.lunar_month),
        lunar_date.lunar_day
    )

