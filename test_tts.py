#!/usr/bin/env python3
import asyncio
import os
from dotenv import load_dotenv
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("test-tts")

# Import the TTS service
from Backend.tts_service import generate_audio_with_elevenlabs

async def test_tts():
    """Test the TTS service with a simple text"""
    # Create audio directory if it doesn't exist
    audio_dir = Path("audio_outputs")
    audio_dir.mkdir(exist_ok=True)
    
    # Test text
    test_text = "This is a test of the ElevenLabs text-to-speech service. If you can hear this, the service is working correctly."
    
    # Output path
    output_path = audio_dir / "test_audio.mp3"
    
    logger.info(f"Testing TTS service with text: {test_text}")
    
    # Generate audio
    success = await generate_audio_with_elevenlabs(test_text, str(output_path))
    
    if success:
        logger.info(f"✅ TTS test successful! Audio saved to {output_path}")
        logger.info(f"File size: {os.path.getsize(output_path)} bytes")
    else:
        logger.error("❌ TTS test failed!")

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    
    # Check for API key
    api_key = os.getenv('ELEVEN_LABS_KEY')
    if not api_key:
        logger.error("ELEVEN_LABS_KEY environment variable not found")
        print("Error: ELEVEN_LABS_KEY environment variable not found")
        print("Please add your ElevenLabs API key to the .env file")
        exit(1)
    
    # Run the test
    asyncio.run(test_tts())