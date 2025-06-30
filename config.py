import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# App Configuration
APP_NAME = "袁天罡称骨算命"
APP_DESC = "基于袁天罡称骨算命法的命理分析应用"
LOGO_PATH = "assets/logo.png"

# Authentication
AUTHENTICATE = True
PREMIUM_PRICE = 9.9  # Price in USD/RMB

# DeepSeek Configuration
DEEPSEEK_ENABLED = True
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")  # Never hardcode API keys!
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")  # Fallback URL
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")  # Default model

# Paths
BONE_POEMS = "data/bone_poems.json"
FATE_DB = "data/fate_db.json"

# Validate Config
if DEEPSEEK_ENABLED and not DEEPSEEK_API_KEY:
    raise ValueError("DeepSeek API key is required when DEEPSEEK_ENABLED=True")
