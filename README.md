# Mon-Reader: Multi-Model OCR and TTS Application
o2GXTpiRUisJhGpe
Mon-Reader is a production-ready web application that extracts text from images using multiple OCR models (EasyOCR, Google Gemini, LLaVA) and converts it to natural speech using ElevenLabs TTS. The application is containerized with Docker and deployed on AWS EC2 for global accessibility.

## 🚀 Features

- **Multi-Model OCR Support**: Compare and use different OCR engines
  - GPU-accelerated EasyOCR for fast local processing
  - Google Gemini 2.5 Pro for advanced text extraction
  - LLaVA multimodal model for contextual understanding
- **Multi-Language Support**: Handles 15+ languages including Arabic, Urdu, and English
- **Text-to-Speech Synthesis**: Natural voice generation with ElevenLabs API
- **Production-Ready Architecture**: Dockerized frontend and backend with nginx
- **Cloud Deployment**: Hosted on AWS EC2 with proper security configurations
- **User-Friendly Interface**: Modern React-based frontend with drag-and-drop upload
- **Batch Processing**: Handle multiple images efficiently
- **Audio Management**: Download and play generated audio files directly

## 📋 Prerequisites

### For Local Development
- Python 3.8 or higher
- Node.js 18+ and npm
- Docker and Docker Compose
- NVIDIA GPU with CUDA support (for EasyOCR)
- Google Gemini API key
- ElevenLabs API key

### For GPU-Accelerated OCR (Optional)
- NVIDIA GPU (tested on RTX 2060)
- CUDA 11.8 or higher
- PyTorch with CUDA support

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/osamaizhar/Mon-Reader.git
cd Mon-Reader
```

### 2. Set Up Environment Variables
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
ELEVEN_LABS_KEY=your_elevenlabs_api_key_here
```

### 3. Local Development Setup

#### Backend Setup
```bash
cd Backend
pip install -r requirements.txt
```

#### Frontend Setup
```bash
cd Frontend
npm install
```

### 4. Docker Setup (Recommended)
```bash
# Build and run with Docker Compose
docker-compose up -d

# The application will be available at:
# - Frontend: http://localhost:3000
# - Backend API: http://localhost:8000
# - API Documentation: http://localhost:8000/docs
```

## 🏃‍♂️ Running the Application

### Local Development
```bash
# Terminal 1: Start the backend
cd Backend
uvicorn main:app --reload --port 8000

# Terminal 2: Start the frontend
cd Frontend
npm start
```

### Docker Deployment
```bash
# Development environment
docker-compose up -d

# Production environment
docker-compose -f docker-compose.prod.yml up -d
```

## 🔧 GPU-Accelerated OCR Setup

For optimal performance with local OCR processing:

```bash
# Install GPU-accelerated dependencies
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install easyocr

# Verify GPU setup
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
```

## 📁 Project Structure

```
Mon-Reader/
├── Backend/
│   ├── main.py                 # FastAPI application
│   ├── ocr_service.py          # Multi-model OCR service
│   ├── tts_service.py          # ElevenLabs TTS service
│   ├── requirements.txt        # Python dependencies
│   └── Dockerfile              # Backend container config
├── Frontend/
│   ├── src/
│   │   ├── App.tsx            # Main React component
│   │   └── components/        # UI components
│   ├── package.json           # Node dependencies
│   └── Dockerfile             # Frontend container config
├── docker-compose.yml         # Development orchestration
├── docker-compose.prod.yml    # Production orchestration
├── .env.example              # Environment variables template
└── README.md                 # This file
```

## 🌐 API Endpoints

- `GET /`: Health check and API information
- `POST /api/extract-text`: Upload and process image with OCR
- `POST /api/generate-audio`: Generate audio from extracted text
- `GET /api/audio/{job_id}`: Download generated audio file
- `POST /api/process-batch`: Process multiple images
- `GET /api/voices`: Get available ElevenLabs voices
- `GET /health`: Application health status
- `GET /docs`: Interactive API documentation (Swagger UI)

## ☁️ AWS Deployment

### EC2 Instance Setup
```bash
# Connect to your EC2 instance
ssh -i your-key.pem ec2-user@your-instance-ip

# Install Docker
sudo yum update -y
sudo yum install docker -y
sudo service docker start
sudo usermod -a -G docker ec2-user

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Clone and run the application
git clone https://github.com/osamaizhar/Mon-Reader.git
cd Mon-Reader
docker-compose -f docker-compose.prod.yml up -d
```

### Security Configuration
Ensure your EC2 security group allows:
- SSH (port 22) from your IP
- HTTP (port 80) from anywhere
- HTTPS (port 443) from anywhere

## 🔍 Model Comparison

The application supports multiple OCR models with different strengths:

| Model | Best For | Speed | Accuracy |
|-------|----------|-------|----------|
| EasyOCR | Simple text, single language | Fast | Good |
| Gemini 2.5 Pro | Complex layouts, multiple languages | Medium | Excellent |
| LLaVA | Contextual understanding, handwriting | Slow | Very Good |

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google Gemini for advanced OCR capabilities
- ElevenLabs for natural text-to-speech synthesis
- The EasyOCR team for GPU-accelerated text extraction
- AWS for reliable cloud infrastructure

## 📧 Contact

- **GitHub**: https://github.com/osamaizhar/Mon-Reader
- **LinkedIn**: https://www.linkedin.com/in/osamaizhar-b4727116a/
- **Apziva**: https://www.apziva.com/

---

*For detailed implementation details and code examples, please refer to the accompanying article.*
