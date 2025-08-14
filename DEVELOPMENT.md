# Development Setup Guide

## Prerequisites

### Required Software
- **Python 3.8+** with pip
- **Node.js 16+** with npm
- **FFmpeg** (for video processing)
- **Tesseract OCR** (for text extraction)
- **Docker & Docker Compose** (for containerized deployment)

### System Dependencies

#### Windows
```powershell
# Install Python dependencies
pip install -r backend/requirements.txt

# Install spaCy English model
python -m spacy download en_core_web_sm

# Install FFmpeg (using Chocolatey)
choco install ffmpeg

# Install Tesseract (using Chocolatey)
choco install tesseract
```

#### macOS
```bash
# Install FFmpeg
brew install ffmpeg

# Install Tesseract
brew install tesseract

# Install Python dependencies
pip install -r backend/requirements.txt

# Install spaCy English model
python -m spacy download en_core_web_sm
```

#### Ubuntu/Debian
```bash
# Update packages
sudo apt update

# Install FFmpeg and Tesseract
sudo apt install ffmpeg tesseract-ocr tesseract-ocr-eng

# Install Python dependencies
pip install -r backend/requirements.txt

# Install spaCy English model
python -m spacy download en_core_web_sm
```

## Local Development

### Backend Setup
```bash
cd backend

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Copy environment file
cp .env.example .env

# Start development server
python app.py
```

The backend will be available at `http://localhost:5000`

### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

The frontend will be available at `http://localhost:3000`

## Docker Development

### Quick Start
```bash
# Build and start all services
docker-compose up --build

# Or use the provided scripts
./start-dev.sh      # Linux/macOS
start-dev.bat       # Windows
```

### Individual Services
```bash
# Backend only
docker build -f Dockerfile.backend -t video-checker-backend ./backend
docker run -p 5000:5000 video-checker-backend

# Frontend only
docker build -f Dockerfile.frontend -t video-checker-frontend ./frontend
docker run -p 80:80 video-checker-frontend
```

## Environment Configuration

### Backend (.env)
```env
FLASK_ENV=development
PORT=5000
UPLOAD_FOLDER=./temp_videos
MAX_CONTENT_LENGTH=1073741824
TESSERACT_CMD=/usr/bin/tesseract
MAX_KEYFRAMES=30
OCR_CONFIDENCE_THRESHOLD=30
LOG_LEVEL=INFO
```

### Frontend
The frontend automatically proxies API requests to the backend during development.

## Testing the Application

### Health Check
```bash
curl http://localhost:5000/api/health
```

### Sample API Request
```bash
curl -X POST http://localhost:5000/api/check_quality \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://your-iconik-share-url",
    "vocabulary": ["CustomWord1", "CustomWord2"]
  }'
```

## Troubleshooting

### Common Issues

1. **FFmpeg not found**
   - Ensure FFmpeg is installed and in your PATH
   - Test with: `ffmpeg -version`

2. **Tesseract not found**
   - Ensure Tesseract is installed and in your PATH
   - Test with: `tesseract --version`
   - Set TESSERACT_CMD environment variable if needed

3. **spaCy model not found**
   - Run: `python -m spacy download en_core_web_sm`

4. **Port conflicts**
   - Backend uses port 5000
   - Frontend development uses port 3000
   - Docker frontend uses port 80

5. **Memory issues with large videos**
   - Adjust MAX_CONTENT_LENGTH in environment
   - Ensure sufficient disk space for temp files

### Logs
- Backend logs are printed to console
- Check Docker logs: `docker-compose logs backend`

## Development Workflow

1. **Make changes** to backend or frontend code
2. **Test locally** with development servers
3. **Test with Docker** before deployment
4. **Check logs** for any issues
5. **Verify API responses** with sample requests

## Production Deployment

For production deployment on platforms like Render:

1. **Use Docker Compose** configuration
2. **Set environment variables** for production
3. **Configure external storage** for temp files
4. **Set up monitoring** and logging
5. **Configure reverse proxy** if needed
