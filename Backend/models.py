from pydantic import BaseModel
from typing import Optional

class OCRResponse(BaseModel):
    success: bool
    extracted_text: Optional[str] = None
    error: Optional[str] = None

class TTSRequest(BaseModel):
    text: str

class TTSResponse(BaseModel):
    success: bool
    audio_url: Optional[str] = None
    error: Optional[str] = None

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None