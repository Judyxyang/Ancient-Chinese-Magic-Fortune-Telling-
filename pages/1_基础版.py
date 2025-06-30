import streamlit as st
from datetime import datetime
import json
from utils.calendar_conv import solar_to_lunar
from utils.bone_calculator import calculate_bone_weight
from utils.deepseek import get_simple_analysis
from config import APP_NAME, BONE_POEMS, DEEPSEEK_ENABLED

# 设置页面
st.set_page_config(page_title=f"{APP_NAME} - 基础版", layout="wide")

# 加载数据
@st.cache_data
def load_poems():
    with open(BONE_POEMS, 'r', encoding='utf-8') as f:
        return json.load(f)
bone_poems = load_poems()

# 语言选择
if 'language' not in st.session_state:
    st.session_state.language = "中文"

def set_language(lang):
    st.session_state.language = lang

# 侧边栏
with st.sidebar:
    st.title(APP_NAME)
    st.radio(
        "语言/Language",
        ["中文", "English"],
        key="lang_radio",
        on_change=lambda: set_language(st.session_state.lang_radio)
    )  # ✅ Correctly closed
    if DEEPSEEK_ENABLED:
        st.checkbox(
            "启用AI分析" if st.session_state.language == "中文" else "Enable AI Analysis",
            key="use_ai",
            help="使用DeepSeek AI提供更深入的分析" if st.session_state.language == "中文" else "Use DeepSeek AI for deeper analysis"
        )

# 主应用
st.title("袁天罡称骨算命" if st.session_state.language == "中文" else "Yuan Tiangang Bone Fortune Telling")
st.caption("基础版" if st.session_state.language == "中文" else "Basic Version")

# 用户输入表单
with st.form("user_info"):
    col1, col2 = st.columns(2)
    
    with col1:
        gender = st.radio(
            "性别" if st.session_state.language == "中文" else "Gender", 
            ("男", "女") if st.session_state.language == "中文" else ("Male", "Female")
        )
        
    with col2:
        birth_date = st.date_input(
            "出生日期" if st.session_state.language == "中文" else "Birth Date",
            datetime(1990, 1, 1),
            format="YYYY/MM/DD"
        )
    
    birth_hour = st.selectbox(
        "出生时辰" if st.session_state.language == "中文" else "Birth Hour",
        ["子时(23-1)", "丑时(1-3)", "寅时(3-5)", "卯时(5-7)", 
         "辰时(7-9)", "巳时(9-11)", "午时(11-13)", "未时(13-15)", 
         "申时(15-17)", "酉时(17-19)", "戌时(19-21)", "亥时(21-23)"]
    )
    
    submitted = st.form_submit_button(
        "开始算命" if st.session_state.language == "中文" else "Calculate Fortune",
        type="primary"
    )

# 计算并显示结果
if submitted:
    st.divider()
    
    # 转换阳历为阴历
    lunar_date = solar_to_lunar(birth_date.year, birth_date.month, birth_date.day)
    
    # 计算称骨重量
    gender_code = 0 if gender == "男" or gender == "Male" else 1
    hour_code = ["子时(23-1)", "丑时(1-3)", "寅时(3-5)", "卯时(5-7)", 
                "辰时(7-9)", "巳时(9-11)", "午时(11-13)", "未时(13-15)", 
                "申时(15-17)", "酉时(17-19)", "戌时(19-21)", "亥时(21-23)"].index(birth_hour)
    
    weight, breakdown = calculate_bone_weight(lunar_date, hour_code, gender_code)
    
    # 显示结果
    st.subheader("📊 算命结果" if st.session_state.language == "中文" else "📊 Fortune Results")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**{'阳历生日' if st.session_state.language == '中文' else 'Solar Date'}**: {birth_date.strftime('%Y-%m-%d')}")
        st.markdown(f"**{'阴历生日' if st.session_state.language == '中文' else 'Lunar Date'}**: 农历{lunar_date[0]}年{lunar_date[1]}月{lunar_date[2]}日")
        st.markdown(f"**{'出生时辰' if st.session_state.language == '中文' else 'Birth Hour'}**: {birth_hour}")
        st.markdown(f"**{'性别' if st.session_state.language == '中文' else 'Gender'}**: {gender}")
    
    with col2:
        st.markdown(f"**{'总骨重' if st.session_state.language == '中文' else 'Total Bone Weight'}**: {weight} {'两' if st.session_state.language == '中文' else 'taels'}")
        st.progress(min(weight / 7.2, 1.0), 
                   text=f"{'命重评分' if st.session_state.language == '中文' else 'Fate Score'}: {int(min(weight / 7.2, 1.0)*100)}/100")
        
        # 显示详细计算
        with st.expander("📝 详细计算" if st.session_state.language == "中文" else "📝 Calculation Details"):
            for item in breakdown:
                st.text(f"{item['item']}: {item['weight']} {'两' if st.session_state.language == '中文' else 'taels'}")
    
    # 显示对应的命理歌谣
    poem = next((p for p in bone_poems if p['min'] <= weight <= p['max']), None)
    if poem:
        st.subheader("📜 命理歌谣" if st.session_state.language == "中文" else "📜 Fate Poem")
        st.write(poem['content_' + ('zh' if st.session_state.language == '中文' else 'en')])
        
        # 简单解读
        st.subheader("📝 简单解读" if st.session_state.language == "中文" else "📝 Brief Interpretation")
        st.write(poem['interpretation_' + ('zh' if st.session_state.language == '中文' else 'en')])
        
        # DeepSeek AI分析
        if DEEPSEEK_ENABLED and st.session_state.get('use_ai', False):
            st.divider()
            st.subheader("🤖 AI深度分析" if st.session_state.language == "中文" else "🤖 AI Deep Analysis")
            
            with st.spinner("AI正在分析您的命理..." if st.session_state.language == "中文" else "AI is analyzing your fate..."):
                analysis = get_simple_analysis(
                    birth_date=birth_date,
                    birth_hour=birth_hour,
                    gender=gender,
                    bone_weight=weight,
                    language=st.session_state.language
                )
                
            st.write(analysis)
            
            st.info("💡 " + ("此分析由DeepSeek AI生成，仅供参考娱乐" if st.session_state.language == "中文" 
                            else "This analysis is generated by DeepSeek AI, for entertainment only"))
