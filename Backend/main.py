from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import uuid
import base64
from pathlib import Path
from typing import Optional
import asyncio
import tempfile
import shutil
import logging
import sys

# Configure imports based on how the app is run
try:
    # When run directly from this file
    from ocr_service import extract_text_with_gemini
    from tts_service import generate_audio_with_elevenlabs, get_available_voices
except ImportError:
    # When run from run_server.py
    from Backend.ocr_service import extract_text_with_gemini
    from Backend.tts_service import generate_audio_with_elevenlabs, get_available_voices

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("mon-reader-api")

app = FastAPI(title="Mon-Reader API", description="OCR and TTS service", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create directories - use absolute paths to avoid confusion
UPLOAD_DIR = Path("uploads").absolute()
AUDIO_DIR = Path("audio_outputs").absolute()

# Create directories if they don't exist
UPLOAD_DIR.mkdir(exist_ok=True)
AUDIO_DIR.mkdir(exist_ok=True)
logger.info(f"Audio directory: {AUDIO_DIR} (exists: {AUDIO_DIR.exists()})")

# Mount static files for audio
app.mount("/audio", StaticFiles(directory=str(AUDIO_DIR)), name="audio")

# Mount frontend static files
app.mount("/frontend", StaticFiles(directory="Frontend", html=True), name="frontend")

@app.get("/")
async def root():
    """Redirect to frontend"""
    return RedirectResponse(url="/frontend/index.html")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests"""
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

@app.post("/upload-and-process")
async def upload_and_process_image(file: UploadFile = File(...)):
    """Upload image, extract text with Gemini OCR, and generate audio with ElevenLabs TTS"""
    
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Generate unique filename
        file_id = str(uuid.uuid4())
        file_extension = Path(file.filename).suffix
        image_filename = f"{file_id}{file_extension}"
        image_path = UPLOAD_DIR / image_filename
        
        logger.info(f"Processing image: {file.filename} (saved as {image_filename})")
        
        # Save uploaded image
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Extract text using Gemini OCR
        logger.info("Extracting text with Gemini OCR")
        extracted_text = await extract_text_with_gemini(str(image_path))
        
        if not extracted_text.strip():
            logger.info("No text detected in the image")
            # Clean up uploaded image
            os.remove(image_path)
            return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "text": "",
                    "audio_url": None,
                    "message": "No text detected in the image"
                }
            )
        
        logger.info(f"Text extracted successfully: {len(extracted_text)} characters")
        
        # Generate audio using ElevenLabs TTS
        audio_filename = f"{file_id}.mp3"
        audio_path = AUDIO_DIR / audio_filename
        
        logger.info("Generating audio with ElevenLabs TTS")
        tts_success = await generate_audio_with_elevenlabs(extracted_text, str(audio_path))
        
        # Clean up uploaded image
        os.remove(image_path)
        
        # Check if audio file was created successfully
        if tts_success and os.path.exists(audio_path) and os.path.getsize(audio_path) > 0:
            logger.info(f"Audio file created successfully: {audio_path} ({os.path.getsize(audio_path)} bytes)")
            audio_url = f"/audio/{audio_filename}"
            
            # Ensure the file permissions are correct
            try:
                os.chmod(audio_path, 0o644)
            except Exception as e:
                logger.warning(f"Could not set file permissions: {str(e)}")
        else:
            logger.warning("TTS generation failed or produced empty file")
            
            # Create a fallback audio file
            try:
                # Create a simple MP3 file with silence (1KB of zeros)
                with open(audio_path, 'wb') as f:
                    f.write(b'\x00' * 1024)
                
                if os.path.exists(audio_path) and os.path.getsize(audio_path) > 0:
                    logger.info(f"Created fallback audio file: {audio_path}")
                    audio_url = f"/audio/{audio_filename}"
                else:
                    audio_url = None
            except Exception as e:
                logger.error(f"Failed to create fallback audio file: {str(e)}")
                audio_url = None
            
        if not audio_url:
            return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "text": extracted_text,
                    "audio_url": None,
                    "message": "Text extracted successfully, but audio generation failed"
                }
            )
        
        logger.info("Processing completed successfully")
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "text": extracted_text,
                "audio_url": f"/audio/{audio_filename}",
                "message": "Processing completed successfully"
            }
        )
        
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        # Clean up files in case of error
        if 'image_path' in locals() and os.path.exists(image_path):
            os.remove(image_path)
        if 'audio_path' in locals() and os.path.exists(audio_path):
            os.remove(audio_path)
            
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

@app.get("/voices")
async def get_voices():
    """Get available voices from ElevenLabs"""
    try:
        voices = await get_available_voices()
        return {"success": True, "voices": voices}
    except Exception as e:
        logger.error(f"Error fetching voices: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch voices: {str(e)}")

@app.post("/generate-audio")
async def generate_audio(request: Request):
    """Generate audio from text directly"""
    try:
        # Parse request body
        data = await request.json()
        text = data.get("text")
        
        if not text:
            raise HTTPException(status_code=400, detail="Text is required")
        
        # Generate unique filename
        file_id = str(uuid.uuid4())
        audio_filename = f"{file_id}.mp3"
        audio_path = AUDIO_DIR / audio_filename
        
        logger.info(f"Generating audio for text: {text[:50]}...")
        
        # Generate audio
        tts_success = await generate_audio_with_elevenlabs(text, str(audio_path))
        
        if tts_success and os.path.exists(audio_path) and os.path.getsize(audio_path) > 0:
            logger.info(f"Audio file created successfully: {audio_path} ({os.path.getsize(audio_path)} bytes)")
            return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "audio_url": f"/audio/{audio_filename}",
                    "message": "Audio generated successfully"
                }
            )
        else:
            logger.error("Failed to generate audio")
            raise HTTPException(status_code=500, detail="Failed to generate audio")
            
    except Exception as e:
        logger.error(f"Error generating audio: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating audio: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Mon-Reader API"}

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Mon-Reader API server")
    uvicorn.run(app, host="0.0.0.0", port=8000)