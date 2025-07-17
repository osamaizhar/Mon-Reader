import base64
import os
import google.generativeai as genai
from PIL import Image
import io
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger("ocr-service")

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
        
        # Configure Gemini API
        genai.configure(api_key=api_key)
        
        # Initialize model - using Gemini 2.5 Pro for OCR
        model = genai.GenerativeModel('gemini-2.5-pro')
        
        logger.info(f"Processing image: {image_path}")
        
        # Read and process image
        with open(image_path, "rb") as f:
            image_data = f.read()
        
        # Validate and potentially resize image
        image = Image.open(io.BytesIO(image_data))
        original_size = image.size
        
        # Resize if image is too large (optimize for API)
        max_size = 2048
        if max(image.size) > max_size:
            logger.info(f"Resizing image from {original_size} to fit within {max_size}x{max_size}")
            image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            
            # Convert back to bytes
            img_buffer = io.BytesIO()
            image.save(img_buffer, format=image.format or 'JPEG')
            image_data = img_buffer.getvalue()
            image = Image.open(io.BytesIO(image_data))
        
        # Create prompt for OCR
        prompt = "Extract all text from this image. Return only the text content, no additional commentary or explanations."
        
        logger.info("Sending image to Gemini API for OCR")
        
        # Call Gemini API with safety settings adjusted for better OCR
        generation_config = {
            "temperature": 0.1,  # Lower temperature for more deterministic results
            "top_p": 0.95,
            "top_k": 40,
        }
        
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE",
            },
        ]
        
        response = model.generate_content(
            [prompt, image],
            generation_config=generation_config,
            safety_settings=safety_settings
        )
        
        if response.text:
            extracted_text = response.text.strip()
            logger.info(f"Successfully extracted {len(extracted_text)} characters of text")
            return extracted_text
        else:
            logger.warning("No text extracted from image")
            return ""
        
    except Exception as e:
        logger.error(f"OCR Error: {str(e)}")
        raise Exception(f"OCR processing failed: {str(e)}")

class OCRService:
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not found")
        genai.configure(api_key=api_key)
        # Using the best available Gemini model for OCR
        self.model = genai.GenerativeModel('gemini-2.5-pro')
        logger.info("OCR Service initialized with Gemini API")
    
    async def extract_text_from_image(self, image_data: bytes, mime_type: str) -> str:
        """Extract text from image using Gemini OCR"""
        try:
            # Validate and potentially resize image
            image = Image.open(io.BytesIO(image_data))
            original_size = image.size
            
            # Resize if image is too large (optimize for API)
            max_size = 2048
            if max(image.size) > max_size:
                logger.info(f"Resizing image from {original_size} to fit within {max_size}x{max_size}")
                image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
                
                # Convert back to bytes
                img_buffer = io.BytesIO()
                image.save(img_buffer, format=image.format or 'JPEG')
                image_data = img_buffer.getvalue()
                image = Image.open(io.BytesIO(image_data))
            
            # Create prompt for OCR
            prompt = "Extract all text from this image. Return only the text content, no additional commentary or explanations."
            
            logger.info("Sending image to Gemini API for OCR")
            
            # Call Gemini API with safety settings adjusted for better OCR
            generation_config = {
                "temperature": 0.1,
                "top_p": 0.95,
                "top_k": 40,
            }
            
            safety_settings = [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_NONE",
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_NONE",
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_NONE",
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_NONE",
                },
            ]
            
            response = self.model.generate_content(
                [prompt, image],
                generation_config=generation_config,
                safety_settings=safety_settings
            )
            
            if response.text:
                extracted_text = response.text.strip()
                logger.info(f"Successfully extracted {len(extracted_text)} characters of text")
                return extracted_text
            else:
                logger.warning("No text extracted from image")
                return ""
            
        except Exception as e:
            logger.error(f"OCR Error: {str(e)}")
            raise Exception(f"OCR processing failed: {str(e)}")

ocr_service = OCRService()