#!/usr/bin/env python3
import os
import sys
import uvicorn
from dotenv import load_dotenv
import logging
import webbrowser
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("mon-reader")

# Load environment variables
load_dotenv()

# Check for required API keys
required_keys = {
    'GEMINI_API_KEY': 'Gemini API key for OCR',
    'ELEVEN_LABS_KEY': 'ElevenLabs API key for TTS'
}

# Create necessary directories
for directory in ["uploads", "audio_outputs"]:
    Path(directory).mkdir(exist_ok=True)
    logger.info(f"Ensured directory exists: {directory}")

# Check for missing API keys
missing_keys = []
for key, description in required_keys.items():
    if not os.getenv(key):
        missing_keys.append(f"{key} ({description})")

if missing_keys:
    logger.error("Missing required environment variables:")
    for key in missing_keys:
        logger.error(f"  - {key}")
    print("\n❌ Error: Missing API keys")
    print("Please add these to your .env file before running the server:")
    for key in missing_keys:
        print(f"  - {key}")
    print("\nYou can copy .env.example to .env and fill in your API keys.")
    sys.exit(1)

def open_browser():
    """Open browser to the application after a short delay"""
    try:
        webbrowser.open("http://localhost:8000")
        logger.info("Opened browser to application")
    except Exception as e:
        logger.error(f"Failed to open browser: {e}")

if __name__ == "__main__":
    print("\n🚀 Starting Mon-Reader API server...")
    print("📚 OCR powered by Google Gemini")
    print("🔊 TTS powered by ElevenLabs")
    print("\n📋 API Documentation: http://localhost:8000/docs")
    print("🌐 Frontend interface: http://localhost:8000")
    print("\n⏳ Starting server, please wait...")
    
    # Import here to check for dependencies
    try:
        import google.generativeai
        import requests
        import fastapi
    except ImportError as e:
        logger.error(f"Missing dependency: {e}")
        print(f"\n❌ Error: Missing dependency: {e}")
        print("Please install required packages:")
        print("pip install -r Backend/requirements.txt")
        sys.exit(1)
    
    # Run the FastAPI server
    try:
        # Open browser after a short delay
        import threading
        import time
        threading.Timer(2.0, open_browser).start()
        
        # Start server
        uvicorn.run(
            "Backend.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except Exception as e:
        logger.error(f"Server error: {e}")
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)