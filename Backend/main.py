from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, JSONResponse
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

from ocr_service import extract_text_with_gemini
from tts_service import generate_audio_with_elevenlabs

app = FastAPI(title="Mon-Reader API", description="OCR and TTS service", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create directories
UPLOAD_DIR = Path("uploads")
AUDIO_DIR = Path("audio_outputs")
UPLOAD_DIR.mkdir(exist_ok=True)
AUDIO_DIR.mkdir(exist_ok=True)

# Mount static files for audio
app.mount("/audio", StaticFiles(directory=str(AUDIO_DIR)), name="audio")

@app.get("/")
async def root():
    return {"message": "Mon-Reader API is running"}

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
        
        # Save uploaded image
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Extract text using Gemini OCR
        extracted_text = await extract_text_with_gemini(str(image_path))
        
        if not extracted_text.strip():
            return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "text": "",
                    "audio_url": None,
                    "message": "No text detected in the image"
                }
            )
        
        # Generate audio using ElevenLabs TTS
        audio_filename = f"{file_id}.mp3"
        audio_path = AUDIO_DIR / audio_filename
        
        await generate_audio_with_elevenlabs(extracted_text, str(audio_path))
        
        # Clean up uploaded image
        os.remove(image_path)
        
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
        # Clean up files in case of error
        if 'image_path' in locals() and os.path.exists(image_path):
            os.remove(image_path)
        if 'audio_path' in locals() and os.path.exists(audio_path):
            os.remove(audio_path)
            
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Mon-Reader API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)