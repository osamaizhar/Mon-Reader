#!/usr/bin/env python3
"""
Example usage of Hugging Face TTS implementation
"""

from huggingface_sesame_tts import HuggingFaceTTS, FacebookMMSTTS
from pathlib import Path

def main():
    print("🎤 Hugging Face TTS Example")
    print("=" * 40)
    
    # Sample text
    text = "Welcome to Hugging Face text to speech synthesis. This is a demonstration of AI-powered voice generation."
    
    try:
        # Method 1: SpeechT5 TTS
        print("\n1️⃣ Using SpeechT5 TTS:")
        tts = HuggingFaceTTS()
        audio = tts.synthesize(text, "example_speecht5.wav")
        print(f"✅ Generated audio with shape: {audio.shape}")
        
        # Method 2: Facebook MMS TTS (alternative)
        print("\n2️⃣ Using Facebook MMS TTS:")
        mms_tts = FacebookMMSTTS(language="eng")
        audio_mms = mms_tts.synthesize(text, "example_mms.wav")
        print(f"✅ Generated audio with shape: {audio_mms.shape}")
        
        print("\n🎉 TTS examples completed successfully!")
        print("Check the generated .wav files in the current directory.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n📋 Required packages:")
        print("pip install transformers datasets soundfile")

if __name__ == "__main__":
    main()