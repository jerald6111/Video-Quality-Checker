import cv2
import pytesseract
import spacy
import os
import tempfile
import logging
from PIL import Image
import numpy as np

logger = logging.getLogger(__name__)

class ContentChecker:
    """Service for performing content quality checks (OCR + spelling/grammar) on video files"""
    
    def __init__(self, custom_vocabulary=None):
        self.custom_vocabulary = set(custom_vocabulary or [])
        self.nlp = None
        self._load_spacy_model()
        
        # Configure Tesseract if path is specified
        tesseract_cmd = os.getenv('TESSERACT_CMD')
        if tesseract_cmd and os.path.exists(tesseract_cmd):
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
    
    def _load_spacy_model(self):
        """Load spaCy model for grammar checking"""
        try:
            # Try to load English model
            self.nlp = spacy.load("en_core_web_sm")
            logger.info("spaCy English model loaded successfully")
        except OSError:
            logger.warning("spaCy English model not found. Grammar checking will be limited.")
            self.nlp = None
    
    def check_video(self, video_path):
        """
        Perform content quality check on video file
        
        Args:
            video_path (str): Path to the video file
            
        Returns:
            dict: Content check results
        """
        try:
            logger.info(f"Starting content check for: {video_path}")
            
            # Extract keyframes from video
            keyframes = self._extract_keyframes(video_path)
            
            if not keyframes:
                return {
                    'status': 'pass',
                    'errors': [],
                    'warnings': ['No keyframes extracted for text analysis'],
                    'text_found': False
                }
            
            # Extract text from keyframes using OCR
            extracted_texts = []
            for timestamp, frame in keyframes:
                text_data = self._extract_text_from_frame(frame, timestamp)
                if text_data['text'].strip():
                    extracted_texts.append(text_data)
            
            if not extracted_texts:
                return {
                    'status': 'pass',
                    'errors': [],
                    'warnings': ['No text detected in video frames'],
                    'text_found': False
                }
            
            # Perform spelling and grammar checks
            errors = []
            for text_data in extracted_texts:
                text_errors = self._check_text_quality(text_data)
                errors.extend(text_errors)
            
            # Determine overall status
            status = 'fail' if errors else 'pass'
            
            result = {
                'status': status,
                'errors': errors,
                'text_found': True,
                'extracted_text_count': len(extracted_texts),
                'total_keyframes': len(keyframes)
            }
            
            logger.info(f"Content check completed. Status: {status}, Errors found: {len(errors)}")
            return result
            
        except Exception as e:
            logger.error(f"Content check failed: {e}")
            return {
                'status': 'fail',
                'errors': [f'Content analysis failed: {str(e)}'],
                'text_found': False
            }
    
    def _extract_keyframes(self, video_path, max_frames=30):
        """
        Extract keyframes from video for text analysis
        
        Args:
            video_path (str): Path to the video file
            max_frames (int): Maximum number of frames to extract
            
        Returns:
            list: List of (timestamp, frame) tuples
        """
        try:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                raise Exception("Could not open video file")
            
            # Get video properties
            fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = total_frames / fps if fps > 0 else 0
            
            if total_frames == 0:
                raise Exception("Video has no frames")
            
            # Calculate frame sampling interval
            if total_frames <= max_frames:
                frame_interval = 1
            else:
                frame_interval = total_frames // max_frames
            
            keyframes = []
            frame_count = 0
            
            while len(keyframes) < max_frames:
                ret, frame = cap.read()
                if not ret:
                    break
                
                if frame_count % frame_interval == 0:
                    timestamp = frame_count / fps if fps > 0 else frame_count
                    
                    # Check if frame likely contains text
                    if self._frame_has_text_potential(frame):
                        keyframes.append((timestamp, frame))
                
                frame_count += 1
            
            cap.release()
            logger.info(f"Extracted {len(keyframes)} keyframes from {total_frames} total frames")
            return keyframes
            
        except Exception as e:
            logger.error(f"Error extracting keyframes: {e}")
            return []
    
    def _frame_has_text_potential(self, frame):
        """
        Quick check to determine if frame might contain text
        
        Args:
            frame: OpenCV frame
            
        Returns:
            bool: True if frame might contain text
        """
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Apply threshold to create binary image
            _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            
            # Find contours
            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Count rectangular contours that might be text
            text_like_contours = 0
            for contour in contours:
                area = cv2.contourArea(contour)
                if 100 < area < 10000:  # Reasonable size for text
                    x, y, w, h = cv2.boundingRect(contour)
                    aspect_ratio = w / h if h > 0 else 0
                    if 0.2 < aspect_ratio < 10:  # Text-like aspect ratio
                        text_like_contours += 1
            
            # If we have some text-like contours, consider it worth processing
            return text_like_contours > 3
            
        except Exception:
            # If analysis fails, assume it might have text
            return True
    
    def _extract_text_from_frame(self, frame, timestamp):
        """
        Extract text from a single frame using OCR
        
        Args:
            frame: OpenCV frame
            timestamp (float): Timestamp in seconds
            
        Returns:
            dict: Extracted text data with timestamp
        """
        try:
            # Preprocess frame for better OCR
            processed_frame = self._preprocess_frame_for_ocr(frame)
            
            # Convert to PIL Image for Tesseract
            pil_image = Image.fromarray(processed_frame)
            
            # Configure Tesseract options
            custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz .,!?:;-()[]{}"\''
            
            # Extract text with confidence scores
            data = pytesseract.image_to_data(
                pil_image, 
                output_type=pytesseract.Output.DICT,
                config=custom_config
            )
            
            # Filter text by confidence
            words = []
            confidences = []
            for i in range(len(data['text'])):
                word = data['text'][i].strip()
                confidence = int(data['conf'][i])
                if word and confidence > 30:  # Only keep words with confidence > 30%
                    words.append(word)
                    confidences.append(confidence)
            
            extracted_text = ' '.join(words)
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            return {
                'text': extracted_text,
                'timestamp': timestamp,
                'timestamp_formatted': self._format_timestamp(timestamp),
                'confidence': avg_confidence,
                'word_count': len(words)
            }
            
        except Exception as e:
            logger.error(f"OCR extraction failed for frame at {timestamp}s: {e}")
            return {
                'text': '',
                'timestamp': timestamp,
                'timestamp_formatted': self._format_timestamp(timestamp),
                'confidence': 0,
                'word_count': 0
            }
    
    def _preprocess_frame_for_ocr(self, frame):
        """
        Preprocess frame to improve OCR accuracy
        
        Args:
            frame: OpenCV frame
            
        Returns:
            numpy.ndarray: Preprocessed frame
        """
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Apply adaptive threshold
        adaptive_thresh = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        
        # Apply morphological operations to clean up
        kernel = np.ones((2, 2), np.uint8)
        cleaned = cv2.morphologyEx(adaptive_thresh, cv2.MORPH_CLOSE, kernel)
        
        return cleaned
    
    def _check_text_quality(self, text_data):
        """
        Check text for spelling and grammar errors
        
        Args:
            text_data (dict): Text data with timestamp
            
        Returns:
            list: List of error dictionaries
        """
        errors = []
        text = text_data['text']
        timestamp = text_data['timestamp']
        timestamp_formatted = text_data['timestamp_formatted']
        
        if not text.strip():
            return errors
        
        # Split text into words for spelling check
        words = text.split()
        
        # Spelling check
        for word in words:
            # Clean word (remove punctuation)
            clean_word = ''.join(char for char in word if char.isalnum())
            if not clean_word:
                continue
            
            # Skip if word is in custom vocabulary
            if clean_word.lower() in self.custom_vocabulary:
                continue
            
            # Skip short words and numbers
            if len(clean_word) < 3 or clean_word.isdigit():
                continue
            
            # Basic spelling check (this is simplified - in production, use a proper spell checker)
            if not self._is_word_spelled_correctly(clean_word):
                suggestion = self._get_spelling_suggestion(clean_word)
                errors.append({
                    'type': 'spelling',
                    'timestamp': timestamp_formatted,
                    'word': clean_word,
                    'suggestion': suggestion,
                    'context': text[:100] + '...' if len(text) > 100 else text
                })
        
        # Grammar check using spaCy
        if self.nlp:
            grammar_errors = self._check_grammar_with_spacy(text, timestamp_formatted)
            errors.extend(grammar_errors)
        
        return errors
    
    def _is_word_spelled_correctly(self, word):
        """
        Basic spelling check (simplified implementation)
        
        Args:
            word (str): Word to check
            
        Returns:
            bool: True if word appears to be spelled correctly
        """
        # This is a simplified implementation
        # In production, you would use a proper spell checking library
        
        # Common correctly spelled words (basic dictionary)
        common_words = {
            'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
            'by', 'from', 'up', 'about', 'into', 'through', 'during', 'before',
            'after', 'above', 'below', 'between', 'among', 'is', 'are', 'was',
            'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does',
            'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must',
            'can', 'this', 'that', 'these', 'those', 'there', 'here', 'where',
            'when', 'why', 'how', 'what', 'which', 'who', 'whom', 'whose'
        }
        
        return word.lower() in common_words or len(word) < 3
    
    def _get_spelling_suggestion(self, word):
        """
        Get spelling suggestion for a word
        
        Args:
            word (str): Misspelled word
            
        Returns:
            str: Suggested correction
        """
        # Simplified suggestion system
        # In production, use a proper spell checker with suggestions
        return f"Check spelling of '{word}'"
    
    def _check_grammar_with_spacy(self, text, timestamp_formatted):
        """
        Check grammar using spaCy
        
        Args:
            text (str): Text to check
            timestamp_formatted (str): Formatted timestamp
            
        Returns:
            list: List of grammar errors
        """
        errors = []
        
        try:
            doc = self.nlp(text)
            
            # Check for incomplete sentences
            sentences = list(doc.sents)
            for sent in sentences:
                sent_text = sent.text.strip()
                
                # Check if sentence ends with proper punctuation
                if len(sent_text) > 10 and not sent_text.endswith(('.', '!', '?')):
                    errors.append({
                        'type': 'grammar',
                        'timestamp': timestamp_formatted,
                        'error': f"Sentence may be incomplete: '{sent_text[:50]}...'",
                        'suggestion': "Check if sentence ends properly"
                    })
                
                # Check for very short sentences that might be fragments
                if len(sent_text.split()) < 2 and len(sent_text) > 1:
                    errors.append({
                        'type': 'grammar',
                        'timestamp': timestamp_formatted,
                        'error': f"Possible sentence fragment: '{sent_text}'",
                        'suggestion': "Check if this is a complete sentence"
                    })
        
        except Exception as e:
            logger.error(f"Grammar check failed: {e}")
        
        return errors
    
    def _format_timestamp(self, seconds):
        """
        Format timestamp in MM:SS format
        
        Args:
            seconds (float): Timestamp in seconds
            
        Returns:
            str: Formatted timestamp
        """
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes}:{seconds:02d}"
