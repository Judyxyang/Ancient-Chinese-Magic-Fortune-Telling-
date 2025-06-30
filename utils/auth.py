import os
import streamlit as st
from config import PREMIUM_PRICE

def check_subscription():
    """检查用户是否订阅了高级版"""
    # 如果设置了跳过订阅检查的环境变量，则直接返回 True
    if os.getenv("SKIP_SUBSCRIPTION", "false").lower() == "true":
        return True
    return st.session_state.get('premium_user', False)

def show_subscribe_button():
    """显示订阅按钮"""
    if st.button(f"订阅高级版 (¥{PREMIUM_PRICE}/月)"):
        st.session_state.premium_user = True
        st.rerun()


