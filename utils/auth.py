import streamlit as st
from config import PREMIUM_PRICE

def check_subscription():
    """检查用户是否订阅了高级版"""
    # 实际应用中应该连接到数据库验证
    return st.session_state.get('premium_user', False)

def show_subscribe_button():
    """显示订阅按钮"""
    if st.button(f"订阅高级版 (¥{PREMIUM_PRICE}/月)"):
        st.session_state.premium_user = True
        st.rerun()

