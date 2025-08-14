<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Video Quality & Content Checker Project

## Project Overview
Advanced web application for analyzing video files from Iconik share links, performing technical quality validation and content quality checking (OCR + spelling/grammar).

## Architecture
- **Backend**: Flask/Python with video processing, OCR, and NLP capabilities
- **Frontend**: React single-page application
- **Deployment**: Docker containerization with Docker Compose
- **Processing**: FFmpeg, Tesseract OCR, OpenCV, spaCy

## Development Status
✅ Project scaffolded and configured
✅ Backend API with mock responses (full functionality requires system dependencies)
✅ React frontend with modern UI
✅ Docker configuration ready
✅ Documentation complete

## Quick Start

### Development Mode
```bash
# Backend (simplified test version)
cd backend
python app_test.py

# Frontend
cd frontend
npm install
npm start
```

### Production Mode
```bash
docker-compose up --build
```

## System Dependencies Required for Full Functionality
- FFmpeg (video processing)
- Tesseract OCR (text extraction)
- OpenCV (computer vision)
- spaCy English model (grammar checking)

## Key Features Implemented
- Video URL submission and validation
- Custom vocabulary support
- Mock API responses for testing
- Comprehensive error handling
- Responsive UI with real-time feedback
- Docker deployment configuration
