from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import logging

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure CORS for production
CORS(app, origins=[
    "https://your-vercel-app.vercel.app",
    "http://localhost:3000",  # For development
    "https://video-quality-checker.vercel.app"  # Update with your actual Vercel URL
])

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 1073741824))  # 1GB
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', './temp_videos')

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy', 
        'message': 'Video Quality Checker API is running',
        'version': '1.0.0',
        'mode': 'production',
        'environment': os.getenv('RENDER_SERVICE_NAME', 'local')
    })

@app.route('/api/check_quality', methods=['POST'])
def check_quality():
    """Main endpoint for video quality checking - production version with mock data"""
    try:
        # Parse request data
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        iconik_url = data.get('url', '').strip()
        custom_vocabulary = data.get('vocabulary', [])
        
        if not iconik_url:
            return jsonify({'error': 'Iconik URL is required'}), 400
        
        # Basic URL validation
        if not iconik_url.startswith(('http://', 'https://')):
            return jsonify({'error': 'Invalid URL format. Please provide a valid HTTP/HTTPS URL.'}), 400
        
        logger.info(f"Processing video quality check for URL: {iconik_url}")
        
        # Enhanced mock response for production demo
        import random
        from datetime import datetime
        
        # Simulate different outcomes based on URL content
        is_pass = 'test-pass' in iconik_url.lower() or random.choice([True, False, True])  # 66% pass rate
        
        if is_pass:
            mock_response = {
                'status': 'pass',
                'technical_status': 'pass',
                'content_status': 'pass',
                'timestamp': datetime.now().isoformat(),
                'technical_metadata': {
                    'resolution': '1920x1080',
                    'frame_rate': 29.97,
                    'codec': 'h264',
                    'codec_profile': 'High',
                    'duration': round(random.uniform(30, 300), 1),
                    'bit_rate': f'{random.uniform(3.0, 10.0):.1f} Mbps',
                    'file_size': f'{random.uniform(50, 500):.1f} MB',
                    'pixel_format': 'yuv420p',
                    'format': 'mp4',
                    'validation_details': {
                        'resolution_check': {
                            'current': '1920x1080',
                            'required': '1920x1080',
                            'pass': True
                        },
                        'frame_rate_check': {
                            'current': 29.97,
                            'valid_rates': [23.976, 24, 25, 29.97, 30, 50, 60],
                            'pass': True
                        },
                        'codec_check': {
                            'current': 'h264',
                            'valid_codecs': ['h264', 'prores', 'h.264'],
                            'pass': True
                        }
                    }
                },
                'content_analysis': {
                    'text_detected': True,
                    'total_keyframes_analyzed': random.randint(20, 50),
                    'frames_with_text': random.randint(5, 15),
                    'spelling_errors': 0,
                    'grammar_errors': 0,
                    'warnings': []
                },
                'errors': [],
                'summary': {
                    'total_errors': 0,
                    'technical_errors': 0,
                    'content_errors': 0,
                    'technical_passed': True,
                    'content_passed': True
                }
            }
        else:
            # Mock failure response
            mock_response = {
                'status': 'fail',
                'technical_status': 'fail',
                'content_status': 'fail',
                'timestamp': datetime.now().isoformat(),
                'technical_metadata': {
                    'resolution': '1280x720',
                    'frame_rate': 15.0,
                    'codec': 'unknown',
                    'duration': round(random.uniform(10, 120), 1),
                    'bit_rate': f'{random.uniform(0.5, 2.0):.1f} Mbps',
                    'file_size': f'{random.uniform(10, 50):.1f} MB'
                },
                'content_analysis': {
                    'text_detected': True,
                    'total_keyframes_analyzed': random.randint(10, 25),
                    'frames_with_text': random.randint(3, 8),
                    'spelling_errors': random.randint(1, 5),
                    'grammar_errors': random.randint(1, 3)
                },
                'errors': [
                    {
                        'type': 'technical',
                        'error': 'Resolution 1280x720 is below minimum requirement of 1920x1080',
                        'timestamp': 'N/A'
                    },
                    {
                        'type': 'technical', 
                        'error': 'Frame rate 15.0 FPS is not in approved list',
                        'timestamp': 'N/A'
                    },
                    {
                        'type': 'spelling',
                        'timestamp': '0:15',
                        'word': 'Exampl',
                        'suggestion': 'Example',
                        'context': 'This is an exampl of text with errors...'
                    },
                    {
                        'type': 'grammar',
                        'timestamp': '0:42',
                        'error': 'Sentence fragment detected',
                        'suggestion': 'Check if sentence is complete'
                    }
                ],
                'recommendations': [
                    {
                        'category': 'technical',
                        'issue': 'Resolution too low',
                        'recommendation': 'Ensure video resolution is at least 1920x1080 (1080p)'
                    },
                    {
                        'category': 'technical',
                        'issue': 'Invalid frame rate',
                        'recommendation': 'Use standard frame rates: 23.976, 24, 25, 29.97, 30, 50, or 60 FPS'
                    },
                    {
                        'category': 'content',
                        'issue': 'Spelling and grammar errors found',
                        'recommendation': 'Review and correct text content in the video'
                    }
                ],
                'summary': {
                    'total_errors': 4,
                    'technical_errors': 2,
                    'content_errors': 2,
                    'technical_passed': False,
                    'content_passed': False
                }
            }
        
        logger.info(f"Mock video quality check completed. Status: {mock_response['status']}")
        return jsonify(mock_response)
                
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

@app.route('/', methods=['GET'])
def root():
    """Root endpoint"""
    return jsonify({
        'message': 'Video Quality Checker API',
        'version': '1.0.0',
        'status': 'running',
        'endpoints': {
            'health': '/api/health',
            'check_quality': '/api/check_quality (POST)'
        }
    })

@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': 'File too large. Maximum size is 1GB'}), 413

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    
    logger.info(f"Starting Video Quality Checker API (Production Mode) on port {port}")
    logger.info("Note: This is a demo version with mock responses.")
    logger.info("For full functionality, deploy with system dependencies: FFmpeg, Tesseract, OpenCV, spaCy")
    
    app.run(host='0.0.0.0', port=port, debug=False)
