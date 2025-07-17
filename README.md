# Mon-Reader: OCR and TTS Application

Mon-Reader is a web application that extracts text from images using Google Gemini OCR and converts it to speech using ElevenLabs TTS.

## Features

- Upload images and extract text using Google Gemini OCR
- Convert extracted text to speech using ElevenLabs TTS
- User-friendly web interface
- Download audio files of the extracted text
- Copy extracted text to clipboard

## Setup

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key
- ElevenLabs API key

### Installation

1. Clone this repository
2. Install the required packages:

```bash
pip install -r Backend/requirements.txt
```

3. Create a `.env` file in the root directory with your API keys:

```
GEMINI_API_KEY=your_gemini_api_key_here
ELEVEN_LABS_KEY=your_elevenlabs_api_key_here
```

### Running the Application

Run the application using:

```bash
python run_server.py
```

The application will be available at:
- Web Interface: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Usage

1. Open the web interface in your browser
2. Upload an image containing text
3. The application will extract the text and generate audio
4. You can listen to the audio, download it, or copy the extracted text

## Project Structure

- `Backend/`: FastAPI backend code
  - `main.py`: Main FastAPI application
  - `ocr_service.py`: Google Gemini OCR service
  - `tts_service.py`: ElevenLabs TTS service
- `Frontend/`: Web interface
  - `index.html`: Main HTML page
  - `script.js`: JavaScript for the web interface
  - `styles.css`: CSS styles
- `uploads/`: Temporary storage for uploaded images
- `audio_outputs/`: Storage for generated audio files

## API Endpoints

- `GET /`: Redirects to the web interface
- `POST /upload-and-process`: Upload and process an image
- `GET /voices`: Get available ElevenLabs voices
- `GET /health`: Health check endpoint
- `GET /docs`: API documentation (Swagger UI)

## License

This project is licensed under the MIT License.