from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import logging

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

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
        'mode': 'development'
    })

@app.route('/api/check_quality', methods=['POST'])
def check_quality():
    """Main endpoint for video quality checking - simplified version"""
    try:
        # Parse request data
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        iconik_url = data.get('url', '').strip()
        custom_vocabulary = data.get('vocabulary', [])
        
        if not iconik_url:
            return jsonify({'error': 'Iconik URL is required'}), 400
        
        # Validate URL format
        if 'iconik' not in iconik_url.lower():
            return jsonify({'error': 'Invalid Iconik URL format'}), 400
        
        logger.info(f"Processing video quality check for URL: {iconik_url}")
        
        # Simplified mock response for testing
        mock_response = {
            'status': 'pass',
            'technical_status': 'pass',
            'content_status': 'pass',
            'timestamp': '2025-08-15T10:30:00Z',
            'technical_metadata': {
                'resolution': '1920x1080',
                'frame_rate': 29.97,
                'codec': 'h264',
                'codec_profile': 'High',
                'duration': 120.5,
                'bit_rate': '5.2 Mbps',
                'file_size': '78.4 MB',
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
                'total_keyframes_analyzed': 25,
                'frames_with_text': 8,
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
        
        logger.info("Mock video quality check completed successfully")
        return jsonify(mock_response)
                
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

@app.route('/api/check_quality_fail', methods=['POST'])
def check_quality_fail():
    """Test endpoint that returns a failure response"""
    try:
        data = request.get_json()
        iconik_url = data.get('url', '').strip() if data else ''
        
        # Mock failure response
        mock_failure = {
            'status': 'fail',
            'technical_status': 'fail',
            'content_status': 'fail',
            'timestamp': '2025-08-15T10:30:00Z',
            'technical_metadata': {
                'resolution': '1280x720',
                'frame_rate': 15.0,
                'codec': 'unknown',
                'duration': 45.2,
                'bit_rate': '0.8 Mbps',
                'file_size': '12.3 MB'
            },
            'content_analysis': {
                'text_detected': True,
                'total_keyframes_analyzed': 15,
                'frames_with_text': 5,
                'spelling_errors': 3,
                'grammar_errors': 2
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
                    'word': 'Haynaku',
                    'suggestion': 'Hay-naku',
                    'context': 'This is a sample text with Haynaku word...'
                },
                {
                    'type': 'grammar',
                    'timestamp': '0:30',
                    'error': 'Sentence may be incomplete',
                    'suggestion': 'Check if sentence ends properly'
                }
            ],
            'recommendations': [
                {
                    'category': 'technical',
                    'issue': 'Resolution too low',
                    'recommendation': 'Ensure video resolution is at least 1920x1080 (1080p)'
                },
                {
                    'category': 'content',
                    'issue': '3 spelling error(s) found',
                    'recommendation': 'Review and correct spelling errors in video text content'
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
        
        return jsonify(mock_failure)
        
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500

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
    debug = os.getenv('FLASK_ENV') == 'development'
    
    logger.info(f"Starting Video Quality Checker API (Test Mode) on port {port}")
    logger.info("Note: This is a simplified version for testing. Full functionality requires:")
    logger.info("- FFmpeg for video processing")
    logger.info("- Tesseract OCR for text extraction") 
    logger.info("- OpenCV for computer vision")
    logger.info("- spaCy for natural language processing")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
