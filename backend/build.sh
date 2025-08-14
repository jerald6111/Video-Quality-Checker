#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Note: For full functionality, you would also need to install system dependencies:
# apt-get update && apt-get install -y ffmpeg tesseract-ocr tesseract-ocr-eng
# python -m spacy download en_core_web_sm

echo "Build completed. Note: This deployment uses the simplified test version."
echo "For full video processing capabilities, additional system dependencies are required."
