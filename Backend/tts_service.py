import os
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

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
            raise ValueError("ELEVEN_LABS_KEY environment variable not found")
        
        # Initialize ElevenLabs client
        client = ElevenLabs(api_key=api_key)
        
        # Generate audio stream
        audio_stream = client.text_to_speech.stream(
            text=text,
            voice_id="JBFqnCBsd6RMkjVDRZzb",  # George voice
            model_id="eleven_multilingual_v2"
        )
        
        # Save audio to file
        with open(output_path, 'wb') as audio_file:
            for chunk in audio_stream:
                if isinstance(chunk, bytes):
                    audio_file.write(chunk)
        
        return True
        
    except Exception as e:
        print(f"Error generating audio: {str(e)}")
        return False

def get_available_voices():
    """Get list of available voices from ElevenLabs"""
    try:
        api_key = os.getenv('ELEVEN_LABS_KEY')
        if not api_key:
            return []
        
        client = ElevenLabs(api_key=api_key)
        voices = client.voices.get_all()
        
        return [{"id": voice.voice_id, "name": voice.name} for voice in voices.voices]
        
    except Exception as e:
        print(f"Error fetching voices: {str(e)}")
        return []