# Mon-Reader - OCR & TTS Application

A modern web application that extracts text from images using Gemini OCR and converts it to speech using ElevenLabs TTS.

## Features

- 🖼️ **Image Upload**: Drag & drop or browse to upload images
- 🔍 **OCR Processing**: Extract text using Google Gemini 2.5 Pro
- 🔊 **Text-to-Speech**: Convert extracted text to audio using ElevenLabs
- 🎵 **Audio Playback**: Play and download generated audio
- 📱 **Responsive Design**: Works on desktop and mobile devices
- ⚡ **Modern UI**: Beautiful, intuitive interface

## Project Structure

```
Mon-Reader/
├── Backend/
│   ├── main.py              # FastAPI application
│   ├── ocr_service.py       # Gemini OCR integration
│   ├── tts_service.py       # ElevenLabs TTS integration
│   ├── config.py            # Configuration settings
│   ├── models.py            # Data models
│   └── requirements.txt     # Backend dependencies
├── Frontend/
│   ├── index.html           # Main HTML file
│   ├── styles.css           # CSS styling
│   └── script.js            # JavaScript functionality
├── requirements1.txt        # New dependencies
├── run_server.py           # Server launcher
├── .env.example            # Environment variables template
└── README_MonReader.md     # This file
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements1.txt
```

### 2. Environment Variables

Copy `.env.example` to `.env` and add your API keys:

```bash
cp .env.example .env
```

Edit `.env` file:
```
GEMINI_API_KEY=your_gemini_api_key_here
ELEVEN_LABS_KEY=your_elevenlabs_api_key_here
```

### 3. Get API Keys

**Gemini API Key:**
1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Create a new API key
3. Copy the key to your `.env` file

**ElevenLabs API Key:**
1. Sign up at [ElevenLabs](https://elevenlabs.io/)
2. Go to your profile settings
3. Copy your API key to your `.env` file

### 4. Run the Application

```bash
python run_server.py
```

### 5. Access the Application

- **Frontend**: Open `Frontend/index.html` in your web browser
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Usage

1. **Upload Image**: Drag and drop an image or click to browse
2. **Process**: Click "Process Image" to extract text and generate audio
3. **View Results**: See extracted text and play/download the audio
4. **New Image**: Click "Process Another Image" to start over

## API Endpoints

### POST `/upload-and-process`
Upload an image and get extracted text with generated audio.

**Request:**
- Form data with image file

**Response:**
```json
{
  "success": true,
  "text": "Extracted text from image",
  "audio_url": "/audio/filename.mp3",
  "message": "Processing completed successfully"
}
```

### GET `/health`
Health check endpoint.

## Supported Image Formats

- JPEG/JPG
- PNG
- GIF
- WebP
- BMP
- TIFF

## Technologies Used

### Backend
- **FastAPI**: Modern Python web framework
- **Google Gemini 2.5 Pro**: Advanced OCR capabilities
- **ElevenLabs**: High-quality text-to-speech
- **Pillow**: Image processing
- **Uvicorn**: ASGI server

### Frontend
- **HTML5**: Modern semantic markup
- **CSS3**: Advanced styling with animations
- **Vanilla JavaScript**: No framework dependencies
- **Font Awesome**: Icon library

## Development

### Running in Development Mode

The server runs with auto-reload enabled by default. Any changes to the backend code will automatically restart the server.

### Adding New Features

1. **Backend**: Add new endpoints in `main.py`
2. **OCR**: Modify `ocr_service.py` for OCR enhancements
3. **TTS**: Update `tts_service.py` for TTS improvements
4. **Frontend**: Edit HTML, CSS, or JS files as needed

## Troubleshooting

### Common Issues

1. **API Key Errors**: Ensure your `.env` file has valid API keys
2. **Port Already in Use**: Change the port in `run_server.py`
3. **CORS Issues**: The backend is configured to allow all origins
4. **File Upload Errors**: Check file size (max 10MB) and format

### Error Messages

- **"GEMINI_API_KEY environment variable not found"**: Add your Gemini API key to `.env`
- **"ELEVEN_LABS_KEY environment variable not found"**: Add your ElevenLabs API key to `.env`
- **"Processing failed"**: Check your API keys and internet connection

## License

This project is open source. Feel free to use and modify as needed.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

**Mon-Reader** - Bringing text to life through AI-powered OCR and TTS technology.