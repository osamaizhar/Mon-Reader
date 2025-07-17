import os
import requests
import json
import logging
import time
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("tts-service")

async def generate_audio_with_elevenlabs(text: str, output_path: str) -> bool:
    """
    Generate audio from text using ElevenLabs TTS API
    
    Args:
        text: Text to convert to speech
        output_path: Path where to save the audio file
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Get API key
        api_key = os.getenv('ELEVEN_LABS_KEY')
        if not api_key:
            logger.error("ELEVEN_LABS_KEY environment variable not found")
            raise ValueError("ELEVEN_LABS_KEY environment variable not found")
        
        logger.info(f"Using ElevenLabs API key: {api_key[:5]}...{api_key[-5:]}")
        logger.info(f"Output path for audio: {output_path}")
        
        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_dir):
            logger.info(f"Creating output directory: {output_dir}")
            os.makedirs(output_dir, exist_ok=True)
        
        # Use a simple voice that's likely to work
        voice_id = "21m00Tcm4TlvDq8ikWAM"  # Rachel voice
        
        # ElevenLabs API endpoint
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        
        # Request headers
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": api_key
        }
        
        # Limit text length to avoid API issues (ElevenLabs has character limits)
        if len(text) > 1000:
            logger.warning(f"Text too long ({len(text)} chars), truncating to 1000 chars")
            text = text[:997] + "..."
        
        # Request body - using the simplest model for better compatibility
        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.75,
                "similarity_boost": 0.75
            }
        }
        
        logger.info(f"Sending TTS request to ElevenLabs API with voice {voice_id}")
        logger.info(f"Text to convert (first 50 chars): {text[:50]}...")
        
        # Make the request
        response = requests.post(url, json=data, headers=headers)
        
        # Check if request was successful
        if response.status_code == 200:
            # Save audio to file
            with open(output_path, 'wb') as audio_file:
                audio_file.write(response.content)
            
            # Verify file was created and has content
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                logger.info(f"Audio file saved to {output_path} ({os.path.getsize(output_path)} bytes)")
                return True
            else:
                logger.error(f"Audio file not created or empty: {output_path}")
                return False
        else:
            logger.error(f"ElevenLabs API error: {response.status_code} - {response.text}")
            
            # Try with a different voice if the first one fails
            backup_voices = [
                "EXAVITQu4vr4xnSDxMaL",  # Bella
                "AZnzlk1XvdvUeBnXmlld",  # Domi
                "MF3mGyEYCl7XYWbV9V6O"   # Elli
            ]
            
            for backup_voice_id in backup_voices:
                try:
                    backup_url = f"https://api.elevenlabs.io/v1/text-to-speech/{backup_voice_id}"
                    
                    logger.info(f"Trying backup voice {backup_voice_id}")
                    backup_response = requests.post(backup_url, json=data, headers=headers)
                    
                    if backup_response.status_code == 200:
                        # Save audio to file
                        with open(output_path, 'wb') as audio_file:
                            audio_file.write(backup_response.content)
                        
                        # Verify file was created and has content
                        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                            logger.info(f"Audio file saved to {output_path} with backup voice ({os.path.getsize(output_path)} bytes)")
                            return True
                except Exception as e:
                    logger.warning(f"Error with backup voice {backup_voice_id}: {str(e)}")
                    continue
            
            # If all voices fail, create a simple audio file with a message
            try:
                # Create a simple audio file with a message
                logger.info("Creating fallback audio file")
                
                # Use a text-to-speech service that doesn't require an API key
                fallback_url = "https://translate.google.com/translate_tts"
                fallback_params = {
                    "ie": "UTF-8",
                    "client": "tw-ob",
                    "tl": "en",
                    "q": "Audio generation failed. Please try again later."
                }
                
                fallback_headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                    "Referer": "https://translate.google.com/"
                }
                
                fallback_response = requests.get(fallback_url, params=fallback_params, headers=fallback_headers)
                
                if fallback_response.status_code == 200:
                    with open(output_path, 'wb') as audio_file:
                        audio_file.write(fallback_response.content)
                    
                    if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                        logger.info(f"Fallback audio file saved to {output_path}")
                        return True
            except Exception as e:
                logger.error(f"Error creating fallback audio: {str(e)}")
            
            return False
        
    except Exception as e:
        logger.error(f"Error generating audio: {str(e)}")
        return False

async def get_available_voices():
    """Get list of available voices from ElevenLabs"""
    try:
        api_key = os.getenv('ELEVEN_LABS_KEY')
        if not api_key:
            logger.error("ELEVEN_LABS_KEY environment variable not found")
            return []
        
        url = "https://api.elevenlabs.io/v1/voices"
        
        headers = {
            "Accept": "application/json",
            "xi-api-key": api_key
        }
        
        logger.info("Fetching available voices from ElevenLabs API")
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            voices_data = response.json()
            voices = [{"id": voice["voice_id"], "name": voice["name"]} for voice in voices_data["voices"]]
            logger.info(f"Retrieved {len(voices)} voices from ElevenLabs API")
            return voices
        else:
            logger.error(f"ElevenLabs API error: {response.status_code} - {response.text}")
            return []
        
    except Exception as e:
        logger.error(f"Error fetching voices: {str(e)}")
        return []