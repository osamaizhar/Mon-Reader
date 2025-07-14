import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    # API Keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    ELEVEN_LABS_KEY = os.getenv("ELEVEN_LABS_KEY")
    
    # File upload settings
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"}
    
    # Directories
    UPLOAD_DIR = "uploads"
    AUDIO_DIR = "audio_outputs"
    
    # TTS Settings
    VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"  # Eleven Labs voice ID
    TTS_MODEL = "eleven_multilingual_v2"
    
    # CORS settings
    ALLOWED_ORIGINS = ["*"]  # In production, specify actual domains

settings = Settings()