import os
from dotenv import load_dotenv

load_dotenv()

# 应用配置
APP_NAME = "袁天罡称骨算命"
APP_DESC = "基于袁天罡称骨算命法的命理分析应用"
LOGO_PATH = "assets/logo.png"

# 认证配置
AUTHENTICATE = True
PREMIUM_PRICE = 9.9  # 高级版价格

# DeepSeek配置
DEEPSEEK_ENABLED = True
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY") # DEEPSEEK_API_KEY sk-8ebe645b7e044e12b5a4712dc39e91b9
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"  # Add this
DEEPSEEK_MODEL = "deepseek-chat"

# 数据文件路径
BONE_POEMS = "data/bone_poems.json"
FATE_DB = "data/fate_db.json"
