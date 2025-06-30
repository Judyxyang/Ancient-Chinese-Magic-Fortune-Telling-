import streamlit as st
from datetime import datetime
import json
from utils.calendar_conv import solar_to_lunar
from utils.bone_calculator import calculate_bone_weight
from utils.deepseek import get_simple_analysis
from config import APP_NAME, BONE_POEMS, DEEPSEEK_ENABLED

# 设置页面
st.set_page_config(
    page_title=f"{APP_NAME} - 基础版",
    layout="wide",
    menu_items={
        'Get Help': 'https://github.com/Yuan-Bone-Fortune',
        'Report a bug': "https://github.com/Yuan-Bone-Fortune/issues",
        'About': f"# {APP_NAME}\n 基于袁天罡称骨算命法的命理分析应用"
    }
)

# 加载数据
@st.cache_data
def load_poems():
    with open(BONE_POEMS, 'r', encoding='utf-8') as f:
        return json.load(f)
bone_poems = load_poems()

# 初始化session状态
if 'language' not in st.session_state:
    st.session_state.language = "中文"
if 'use_ai' not in st.session_state:
    st.session_state.use_ai = False

# 语言切换回调
def set_language():
    st.session_state.language = st.session_state.lang_radio

# 侧边栏
with st.sidebar:
    st.image("assets/logo.png", width=200)
    st.title(APP_NAME)
    
    # 语言选择
    st.radio(
        "语言/Language",
        ["中文", "English"],
        key="lang_radio",
        index=0 if st.session_state.language == "中文" else 1,
        on_change=set_language
    )
    
    # AI分析开关
    if DEEPSEEK_ENABLED:
        st.toggle(
            "启用AI分析" if st.session_state.language == "中文" else "Enable AI Analysis",
            key="use_ai",
            help="使用DeepSeek AI提供更深入的分析" if st.session_state.language == "中文" 
                 else "Use DeepSeek AI for deeper analysis"
        )
    
    st.divider()
    st.page_link("pages/2_高级版.py", 
                label="升级到高级版 →" if st.session_state.language == "中文" else "Upgrade to Premium →",
                icon="💎")

# 主应用标题
st.title("袁天罡称骨算命" if st.session_state.language == "中文" else "Yuan Tiangang Bone Fortune Telling")
st.caption("基础版" if st.session_state.language == "中文" else "Basic Version")

# 用户输入表单
with st.form("user_info"):
    col1, col2 = st.columns(2)
    
    with col1:
        gender = st.radio(
            "性别" if st.session_state.language == "中文" else "Gender", 
            ("男", "女") if st.session_state.language == "中文" else ("Male", "Female"),
            index=0,
            help="性别会影响命重计算" if st.session_state.language == "中文" 
                 else "Gender affects bone weight calculation"
        )
        
    with col2:
        birth_date = st.date_input(
            "出生日期" if st.session_state.language == "中文" else "Birth Date",
            datetime(1990, 1, 1),
            format="YYYY/MM/DD",
            help="请输入公历(阳历)日期" if st.session_state.language == "中文" 
                 else "Please enter solar calendar date"
        )
    
    birth_hour = st.selectbox(
        "出生时辰" if st.session_state.language == "中文" else "Birth Hour",
        ["子时(23-1)", "丑时(1-3)", "寅时(3-5)", "卯时(5-7)", 
         "辰时(7-9)", "巳时(9-11)", "午时(11-13)", "未时(13-15)", 
         "申时(15-17)", "酉时(17-19)", "戌时(19-21)", "亥时(21-23)"],
        help="请选择最接近的时辰" if st.session_state.language == "中文" 
             else "Select the closest time period"
    )
    
    submitted = st.form_submit_button(
        "开始算命" if st.session_state.language == "中文" else "Calculate Fortune",
        type="primary",
        use_container_width=True
    )

# 计算并显示结果
if submitted:
    st.divider()
    
    try:
        # 转换阳历为阴历
        lunar_date = solar_to_lunar(birth_date.year, birth_date.month, birth_date.day)
        
        # 计算称骨重量
        gender_code = 0 if gender == "男" or gender == "Male" else 1
        hour_code = ["子时(23-1)", "丑时(1-3)", "寅时(3-5)", "卯时(5-7)", 
                    "辰时(7-9)", "巳时(9-11)", "午时(11-13)", "未时(13-15)", 
                    "申时(15-17)", "酉时(17-19)", "戌时(19-21)", "亥时(21-23)"].index(birth_hour)
        
        weight, breakdown = calculate_bone_weight(lunar_date, hour_code, gender_code)
        
        # 显示结果卡片
        with st.container(border=True):
            st.subheader("📊 " + ("算命结果" if st.session_state.language == "中文" else "Fortune Results"))
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**{'阳历生日' if st.session_state.language == '中文' else 'Solar Date'}**: {birth_date.strftime('%Y-%m-%d')}")
                st.markdown(f"**{'阴历生日' if st.session_state.language == '中文' else 'Lunar Date'}**: 农历{lunar_date[0]}年{lunar_date[1]}月{lunar_date[2]}日")
                st.markdown(f"**{'出生时辰' if st.session_state.language == '中文' else 'Birth Hour'}**: {birth_hour}")
                st.markdown(f"**{'性别' if st.session_state.language == '中文' else 'Gender'}**: {gender}")
            
            with col2:
                st.markdown(f"**{'总骨重' if st.session_state.language == '中文' else 'Total Bone Weight'}**: {weight} {'两' if st.session_state.language == '中文' else 'taels'}")
                st.progress(
                    min(weight / 7.2, 1.0), 
                    text=f"{'命重评分' if st.session_state.language == '中文' else 'Fate Score'}: {int(min(weight / 7.2, 1.0)*100)}/100"
                )
                
                # 显示详细计算
                with st.expander("📝 " + ("详细计算" if st.session_state.language == "中文" else "Calculation Details")):
                    for item in breakdown:
                        st.text(f"{item['item']}: {item['weight']} {'两' if st.session_state.language == '中文' else 'taels'}")
        
        # 显示对应的命理歌谣
        poem = next((p for p in bone_poems if p['min'] <= weight <= p['max']), None)
        if poem:
            with st.container(border=True):
                st.subheader("📜 " + ("命理歌谣" if st.session_state.language == "中文" else "Fate Poem"))
                st.write(poem['content_' + ('zh' if st.session_state.language == '中文' else 'en')])
                
                # 简单解读
                st.subheader("📝 " + ("简单解读" if st.session_state.language == "中文" else "Brief Interpretation"))
                st.write(poem['interpretation_' + ('zh' if st.session_state.language == '中文' else 'en')])
                
                # DeepSeek AI分析
                if DEEPSEEK_ENABLED and st.session_state.use_ai:
                    st.divider()
                    st.subheader("🤖 " + ("AI深度分析" if st.session_state.language == "中文" else "AI Deep Analysis"))
                    
                    with st.spinner("AI正在分析您的命理..." if st.session_state.language == "中文" else "AI is analyzing your fate..."):
                        analysis = get_simple_analysis(
                            birth_date=birth_date,
                            birth_hour=birth_hour,
                            gender=gender,
                            bone_weight=weight,
                            language=st.session_state.language
                        )
                        
                    st.write(analysis)
                    
                    st.info("💡 " + (
                        "此分析由DeepSeek AI生成，仅供参考娱乐" if st.session_state.language == "中文" 
                        else "This analysis is generated by DeepSeek AI, for entertainment only"
                    ))
    
    except Exception as e:
        st.error("计算错误，请检查输入数据" if st.session_state.language == "中文" else "Calculation error, please check input data")
        st.error(str(e))

# 页脚
st.divider()
footer = """
<div style="text-align: center; color: grey; font-size: 0.8em;">
    <p>""" + ("仅供娱乐参考 · 命运掌握在自己手中" if st.session_state.language == "中文" 
              else "For entertainment only · Fate is in your own hands") + """</p>
    <p>© 2024 """ + APP_NAME + """ · <a href="https://github.com/Yuan-Bone-Fortune" target="_blank">GitHub</a></p>
</div>
"""
st.markdown(footer, unsafe_allow_html=True)