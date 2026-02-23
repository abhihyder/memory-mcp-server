
import os
from dotenv import load_dotenv

load_dotenv()

class AppConfig:
    
    MEM0_PROVIDER: str | None = os.getenv("MEM0_PROVIDER")
    
    MEM0_API_KEY: str | None = os.getenv("MEM0_API_KEY")
    
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
    
app_config = AppConfig()