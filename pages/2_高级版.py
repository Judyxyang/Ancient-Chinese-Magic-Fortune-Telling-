import streamlit as st
from datetime import datetime
import json
from utils.calendar_conv import solar_to_lunar
from utils.bone_calculator import calculate_bone_weight
from utils.deepseek import get_premium_analysis
from utils.auth import check_subscription
from config import APP_NAME, PREMIUM_PRICE, BONE_POEMS, DEEPSEEK_ENABLED
# ✅ 临时定义（用于测试）
# def check_subscription():
#     return True

# 认证检查
# ===== 跳过订阅检查（测试阶段） =====
# if not check_subscription():
#     st.warning(f"请订阅高级版以使用此功能 (¥{PREMIUM_PRICE}/月)")
#     st.stop()
# =====================================
# import os
# SKIP_SUBSCRIPTION = os.getenv("SKIP_SUBSCRIPTION", "false").lower() == "true"

# if not SKIP_SUBSCRIPTION and not check_subscription():
#     st.warning(f"请订阅高级版以使用此功能 (¥{PREMIUM_PRICE}/月)")
#     st.stop()


# 设置页面
st.set_page_config(page_title=f"{APP_NAME} - 高级版", layout="wide")

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
    )
    st.success("✨ " + ("您已订阅高级版" if st.session_state.language == "中文" else "You have Premium subscription"))

# 主应用
st.title("袁天罡称骨算命" if st.session_state.language == "中文" else "Yuan Tiangang Bone Fortune Telling")
st.caption("✨ " + ("高级版 - 全面命理分析" if st.session_state.language == "中文" else "Premium - Comprehensive Analysis"))

# 用户输入表单
with st.form("premium_user_info"):
    col1, col2 = st.columns(2)
    
    with col1:
        gender = st.radio(
            "性别" if st.session_state.language == "中文" else "Gender", 
            ("男", "女") if st.session_state.language == "中文" else ("Male", "Female")
        )
        
        birth_date = st.date_input(
            "出生日期" if st.session_state.language == "中文" else "Birth Date",
            datetime(1990, 1, 1),
            format="YYYY/MM/DD"
        )
    
    with col2:
        birth_hour = st.selectbox(
            "出生时辰" if st.session_state.language == "中文" else "Birth Hour",
            ["子时(23-1)", "丑时(1-3)", "寅时(3-5)", "卯时(5-7)", 
             "辰时(7-9)", "巳时(9-11)", "午时(11-13)", "未时(13-15)", 
             "申时(15-17)", "酉时(17-19)", "戌时(19-21)", "亥时(21-23)"]
        )
        
        birth_minute = st.slider(
            "出生分钟" if st.session_state.language == "中文" else "Birth Minute",
            0, 59, 0
        )
    
    # 高级信息
    with st.expander("🔮 " + ("高级信息(可选)" if st.session_state.language == "中文" else "Advanced Info (Optional)")):
        col3, col4 = st.columns(2)
        with col3:
            birth_place = st.text_input(
                "出生地" if st.session_state.language == "中文" else "Birth Place",
                help="输入出生城市有助于更精确分析" if st.session_state.language == "中文" else "Enter birth city for more accurate analysis"
            )
        with col4:
            current_city = st.text_input(
                "现居地" if st.session_state.language == "中文" else "Current City",
                help="输入现居城市有助于分析运势" if st.session_state.language == "中文" else "Enter current city for fortune analysis"
            )
    
    submitted = st.form_submit_button(
        "开始高级分析" if st.session_state.language == "中文" else "Start Premium Analysis",
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
    
    # 显示基础结果
    st.subheader("📊 " + ("基本命理分析" if st.session_state.language == "中文" else "Basic Fate Analysis"))
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**{'阳历生日' if st.session_state.language == '中文' else 'Solar Date'}**: {birth_date.strftime('%Y-%m-%d')}")
        st.markdown(f"**{'阴历生日' if st.session_state.language == '中文' else 'Lunar Date'}**: 农历{lunar_date[0]}年{lunar_date[1]}月{lunar_date[2]}日")
        st.markdown(f"**{'出生时间' if st.session_state.language == '中文' else 'Birth Time'}**: {birth_hour}:{birth_minute:02d}")
    
    with col2:
        st.markdown(f"**{'总骨重' if st.session_state.language == '中文' else 'Total Bone Weight'}**: {weight} {'两' if st.session_state.language == '中文' else 'taels'}")
        st.progress(min(weight / 7.2, 1.0), 
                   text=f"{'命重评分' if st.session_state.language == '中文' else 'Fate Score'}: {int(min(weight / 7.2, 1.0)*100)}/100")
    
    # 显示命理歌谣
    poem = next((p for p in bone_poems if p['min'] <= weight <= p['max']), None)
    if poem:
        st.subheader("📜 " + ("命理歌谣" if st.session_state.language == "中文" else "Fate Poem"))
        st.write(poem['content_' + ('zh' if st.session_state.language == '中文' else 'en')])
    
    # DeepSeek AI高级分析
    st.divider()
    st.subheader("🔮 " + ("高级命理分析" if st.session_state.language == "中文" else "Premium Fate Analysis"))
    
    with st.spinner("AI正在生成详细命理分析..." if st.session_state.language == "中文" else "AI is generating detailed analysis..."):
        analysis = get_premium_analysis(
            birth_date=birth_date,
            birth_time=f"{birth_hour}:{birth_minute:02d}",
            gender=gender,
            bone_weight=weight,
            birth_place=birth_place,
            current_city=current_city,
            language=st.session_state.language
        )
    
    # 显示分析结果
    tabs = st.tabs([
        "🌟 " + ("总体运势" if st.session_state.language == "中文" else "Overview"),
        "💑 " + ("婚姻感情" if st.session_state.language == "中文" else "Marriage"),
        "💼 " + ("事业财富" if st.session_state.language == "中文" else "Career"),
        "🏥 " + ("健康养生" if st.session_state.language == "中文" else "Health"),
        "📅 " + ("流年运势" if st.session_state.language == "中文" else "Yearly Luck")
    ])
    
    with tabs[0]:
        st.write(analysis.get("overview", ""))
        st.image("assets/life_path.png", width=300)
        
    with tabs[1]:
        st.write(analysis.get("marriage", ""))
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.metric(
                "婚姻指数" if st.session_state.language == "中文" else "Marriage Score", 
                analysis.get("marriage_score", "75/100")
            )
        with col_m2:
            st.metric(
                "最佳婚期" if st.session_state.language == "中文" else "Best Marriage Period", 
                analysis.get("best_marriage_years", "28-32岁" if st.session_state.language == "中文" else "Age 28-32")
            )
    
    with tabs[2]:
        st.write(analysis.get("career", ""))
        st.write("### " + ("适合职业" if st.session_state.language == "中文" else "Suitable Careers"))
        st.write(analysis.get("suitable_careers", ""))
        
    with tabs[3]:
        st.write(analysis.get("health", ""))
        st.write("### " + ("健康建议" if st.session_state.language == "中文" else "Health Advice"))
        st.write(analysis.get("health_advice", ""))
    
    with tabs[4]:
        st.write(analysis.get("yearly_luck", ""))
        st.write("### " + ("未来十年运势" if st.session_state.language == "中文" else "Next 10 Years"))
        st.write(analysis.get("next_decade", ""))
    
    st.info("✨ " + ("此高级分析由DeepSeek AI生成，结合了传统命理学和现代数据分析" if st.session_state.language == "中文" 
                    else "This premium analysis is generated by DeepSeek AI, combining traditional fortune telling with modern data analysis"))
