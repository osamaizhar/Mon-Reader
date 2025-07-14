import base64
import os
from google import genai
from PIL import Image
import io
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def extract_text_with_gemini(image_path: str) -> str:
    """
    Extract text from image using Gemini OCR API
    
    Args:
        image_path: Path to the image file
        
    Returns:
        str: Extracted text from the image
    """
    try:
        # Get API key
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not found")
        
        # Initialize Gemini client
        client = genai.Client()
        
        # Read and process image
        with open(image_path, "rb") as f:
            image_data = f.read()
        
        # Validate and potentially resize image
        image = Image.open(io.BytesIO(image_data))
        
        # Resize if image is too large (optimize for API)
        max_size = 2048
        if max(image.size) > max_size:
            image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            
            # Convert back to bytes
            img_buffer = io.BytesIO()
            image.save(img_buffer, format=image.format or 'JPEG')
            image_data = img_buffer.getvalue()
        
        # Encode image to base64
        image_b64 = base64.b64encode(image_data).decode()
        
        # Determine MIME type
        mime_type = "image/jpeg"
        if image_path.lower().endswith('.png'):
            mime_type = "image/png"
        elif image_path.lower().endswith('.gif'):
            mime_type = "image/gif"
        elif image_path.lower().endswith('.webp'):
            mime_type = "image/webp"
        
        # Call Gemini API
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=[
                {
                    "role": "user",
                    "parts": [
                        {
                            "text": "Extract all text from this image. Return only the text content, no additional commentary or explanations."
                        },
                        {
                            "inline_data": {
                                "mime_type": mime_type,
                                "data": image_b64
                            }
                        }
                    ]
                }
            ]
        )
        
        extracted_text = response.text.strip()
        return extracted_text
        
    except Exception as e:
        raise Exception(f"OCR processing failed: {str(e)}")

class OCRService:
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not found")
        self.client = genai.Client()
    
    async def extract_text_from_image(self, image_data: bytes, mime_type: str) -> str:
        """Extract text from image using Gemini OCR"""
        try:
            # Validate and potentially resize image
            image = Image.open(io.BytesIO(image_data))
            
            # Resize if image is too large (optimize for API)
            max_size = 2048
            if max(image.size) > max_size:
                image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
                
                # Convert back to bytes
                img_buffer = io.BytesIO()
                image.save(img_buffer, format=image.format or 'JPEG')
                image_data = img_buffer.getvalue()
            
            # Encode image to base64
            image_b64 = base64.b64encode(image_data).decode()
            
            # Call Gemini API
            response = self.client.models.generate_content(
                model="gemini-2.5-pro",
                contents=[
                    {
                        "role": "user",
                        "parts": [
                            {
                                "text": "Extract all text from this image. Return only the text content, no additional commentary or explanations."
                            },
                            {
                                "inline_data": {
                                    "mime_type": mime_type,
                                    "data": image_b64
                                }
                            }
                        ]
                    }
                ]
            )
            
            extracted_text = response.text.strip()
            return extracted_text
            
        except Exception as e:
            raise Exception(f"OCR processing failed: {str(e)}")

ocr_service = OCRService()