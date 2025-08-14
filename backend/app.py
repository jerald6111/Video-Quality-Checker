from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import tempfile
import shutil
from services.video_downloader import VideoDownloader
from services.technical_checker import TechnicalChecker
from services.content_checker import ContentChecker
from services.report_generator import ReportGenerator
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
    return jsonify({'status': 'healthy', 'message': 'Video Quality Checker API is running'})

@app.route('/api/check_quality', methods=['POST'])
def check_quality():
    """Main endpoint for video quality checking"""
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
        
        # Create temporary directory for this request
        with tempfile.TemporaryDirectory(dir=UPLOAD_FOLDER) as temp_dir:
            try:
                # Step 1: Download video
                logger.info("Step 1: Downloading video...")
                downloader = VideoDownloader()
                video_path = downloader.download_from_iconik(iconik_url, temp_dir)
                
                if not video_path or not os.path.exists(video_path):
                    return jsonify({'error': 'Failed to download video from Iconik URL'}), 400
                
                # Step 2: Technical quality check
                logger.info("Step 2: Performing technical quality check...")
                technical_checker = TechnicalChecker()
                technical_result = technical_checker.check_video(video_path)
                
                # Step 3: Content quality check
                logger.info("Step 3: Performing content quality check...")
                content_checker = ContentChecker(custom_vocabulary)
                content_result = content_checker.check_video(video_path)
                
                # Step 4: Generate report
                logger.info("Step 4: Generating report...")
                report_generator = ReportGenerator()
                final_report = report_generator.generate_report(
                    technical_result, 
                    content_result
                )
                
                logger.info("Video quality check completed successfully")
                return jsonify(final_report)
                
            except Exception as e:
                logger.error(f"Error during processing: {str(e)}")
                return jsonify({'error': f'Processing failed: {str(e)}'}), 500
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

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
    
    logger.info(f"Starting Video Quality Checker API on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
