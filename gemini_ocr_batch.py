#!/usr/bin/env python3
import os
from pathlib import Path
from google import genai

def extract_text_from_images():
    # Initialize the Gemini client
    client = genai.Client()
    
    # Define paths
    images_dir = Path("part_2_images")
    output_dir = Path("gemini 2.5 pro/extracted_text")
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Process each image file
    for image_file in images_dir.glob("*.jpg"):
        print(f"Processing {image_file.name}...")
        
        try:
            # Read the image file
            with open(image_file, "rb") as f:
                image_data = f.read()
            
            # Create the prompt for OCR
            import base64
            image_b64 = base64.b64encode(image_data).decode()
            
            response = client.models.generate_content(
                model="gemini-2.5-pro",
                contents=[
                    {
                        "role": "user",
                        "parts": [
                            {
                                "text": "Extract all text from this image. Return only the text content, no additional commentary."
                            },
                            {
                                "inline_data": {
                                    "mime_type": "image/jpeg",
                                    "data": image_b64
                                }
                            }
                        ]
                    }
                ]
            )
            
            # Save extracted text to file
            output_file = output_dir / f"{image_file.stem}_extracted.txt"
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(response.text)
            
            print(f"✓ Extracted text saved to {output_file}")
            
        except Exception as e:
            print(f"✗ Error processing {image_file.name}: {str(e)}")

if __name__ == "__main__":
    extract_text_from_images()
    