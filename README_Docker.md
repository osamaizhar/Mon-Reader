# Mon-Reader Docker Deployment Guide

This guide explains how to run Mon-Reader using Docker containers.

## Prerequisites

- Docker and Docker Compose installed on your system
- API keys for Google Gemini and ElevenLabs

## Quick Start

1. **Clone the repository and navigate to the project directory**

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your API keys:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
   ```

3. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - Frontend: http://localhost
   - Backend API: http://localhost:8000

## Architecture

The application consists of two services:

### Backend Service
- **Technology**: FastAPI (Python)
- **Port**: 8000
- **Features**: OCR with Google Gemini, TTS with ElevenLabs
- **Volumes**: Persistent storage for uploads and audio files

### Frontend Service  
- **Technology**: Nginx serving static files
- **Port**: 80
- **Features**: Responsive web interface, API proxy

## Docker Commands

### Build and Start Services
```bash
# Build and start in detached mode
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Development Commands
```bash
# Rebuild specific service
docker-compose build backend
docker-compose build frontend

# Restart specific service
docker-compose restart backend
docker-compose restart frontend

# Execute commands in running container
docker-compose exec backend bash
docker-compose exec frontend sh
```

### Cleanup
```bash
# Stop and remove containers, networks
docker-compose down

# Remove containers, networks, and volumes
docker-compose down -v

# Remove images as well
docker-compose down --rmi all
```

## Configuration

### Environment Variables
- `GOOGLE_API_KEY`: Required for OCR functionality
- `ELEVENLABS_API_KEY`: Required for TTS functionality  
- `ELEVENLABS_VOICE_ID`: Optional voice selection
- `DEBUG`: Set to `true` for development
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)

### Volumes
- `./Backend/uploads`: Temporary image uploads
- `./Backend/audio_outputs`: Generated audio files

### Ports
- `80`: Frontend (Nginx)
- `8000`: Backend API (FastAPI)

## Production Deployment

For production deployment:

1. **Use environment-specific configuration**
   ```bash
   # Create production environment file
   cp .env.example .env.prod
   # Edit .env.prod with production values
   ```

2. **Update docker-compose for production**
   ```yaml
   # Add to docker-compose.yml
   env_file:
     - .env.prod
   ```

3. **Enable HTTPS** (recommended)
   - Add SSL certificates
   - Configure nginx for HTTPS
   - Update ports and proxy settings

4. **Resource limits**
   ```yaml
   # Add to services in docker-compose.yml
   deploy:
     resources:
       limits:
         memory: 1G
         cpus: '0.5'
   ```

## Troubleshooting

### Common Issues

1. **API Connection Failed**
   - Check if backend container is running: `docker-compose ps`
   - View backend logs: `docker-compose logs backend`
   - Verify environment variables are set

2. **File Upload Issues**
   - Check volume mounts are correct
   - Verify file permissions
   - Check available disk space

3. **Audio Generation Failed**
   - Verify ElevenLabs API key is valid
   - Check API quota/limits
   - Review backend logs for errors

### Health Checks
```bash
# Check backend health
curl http://localhost:8000/health

# Check frontend
curl http://localhost
```

### Logs
```bash
# View all logs
docker-compose logs

# Follow specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

## Development

For local development with Docker:

1. **Use development override**
   ```bash
   # Create docker-compose.override.yml for development settings
   docker-compose -f docker-compose.yml -f docker-compose.override.yml up
   ```

2. **Mount source code for live reload**
   ```yaml
   # In docker-compose.override.yml
   services:
     backend:
       volumes:
         - ./Backend:/app
       command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

## Security Considerations

- Keep API keys secure and never commit them to version control
- Use HTTPS in production
- Implement rate limiting for API endpoints
- Regular security updates for base images
- Consider using Docker secrets for sensitive data

## Performance Optimization

- Use multi-stage builds for smaller images
- Implement caching strategies
- Configure resource limits
- Use nginx for static file serving and caching
- Consider using a reverse proxy like Traefik for load balancing