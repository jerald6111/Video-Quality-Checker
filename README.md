# Advanced Video Quality & Content Checker for Iconik Links

A comprehensive web application that analyzes video files from Iconik share links, performing both technical quality checks and content quality checks (spelling & grammar) with timestamped error reporting.

## Features

- **Web Interface**: Simple single-page application for submitting Iconik share URLs
- **Technical Quality Check**: Validates video resolution, frame rate, and codec standards
- **Content Quality Check**: OCR-based text extraction with spelling and grammar validation
- **Custom Vocabulary**: Support for user-defined vocabulary to prevent false positives
- **Timestamped Reports**: Detailed error reports with exact timestamps
- **Docker Support**: Containerized for easy deployment

## Architecture

### Frontend (React)
- Single-page interface for URL submission
- Custom vocabulary input
- Real-time processing status
- Results display

### Backend (Flask/Python)
- RESTful API for video processing
- Video download from Iconik shares
- FFmpeg/FFprobe for technical analysis
- OpenCV + Tesseract for OCR
- spaCy for grammar checking

## Technical Requirements

### Video Standards
- **Resolution**: 1920x1080 (1080p) or higher
- **Frame Rate**: 23.976, 24, 25, 29.97, 30, 50, or 60 FPS
- **Codec**: H.264 or ProRes

## API Response Format

```json
{
  "status": "fail",
  "technical_status": "pass",
  "content_status": "fail",
  "technical_metadata": {
    "resolution": "1920x1080",
    "frame_rate": "29.97",
    "codec": "H.264"
  },
  "errors": [
    {
      "type": "spelling",
      "timestamp": "0:15",
      "word": "Haynaku",
      "suggestion": "Hay-naku"
    },
    {
      "type": "grammar",
      "timestamp": "0:30",
      "error": "The sentence is incomplete."
    }
  ]
}
```

## Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- FFmpeg
- Tesseract OCR

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

### Docker Deployment
```bash
docker-compose up --build
```

## Development

### Project Structure
```
video-quality-checker/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── services/
│   │   ├── video_downloader.py
│   │   ├── technical_checker.py
│   │   ├── content_checker.py
│   │   └── report_generator.py
│   └── utils/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   └── App.js
│   ├── package.json
│   └── public/
├── docker-compose.yml
├── Dockerfile.backend
├── Dockerfile.frontend
└── README.md
```

## Environment Variables

```env
FLASK_ENV=development
UPLOAD_FOLDER=./temp_videos
MAX_CONTENT_LENGTH=1073741824
TESSERACT_CMD=/usr/bin/tesseract
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License
