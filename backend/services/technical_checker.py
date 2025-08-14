import subprocess
import json
import os
import logging

logger = logging.getLogger(__name__)

class TechnicalChecker:
    """Service for performing technical quality checks on video files"""
    
    def __init__(self):
        self.required_standards = {
            'min_resolution': (1920, 1080),  # 1080p minimum
            'valid_frame_rates': [23.976, 24, 25, 29.97, 30, 50, 60],
            'valid_codecs': ['h264', 'prores', 'h.264']
        }
    
    def check_video(self, video_path):
        """
        Perform technical quality check on video file
        
        Args:
            video_path (str): Path to the video file
            
        Returns:
            dict: Technical check results
        """
        try:
            logger.info(f"Starting technical check for: {video_path}")
            
            # Extract video metadata using FFprobe
            metadata = self._extract_metadata(video_path)
            
            # Validate against standards
            validation_result = self._validate_metadata(metadata)
            
            result = {
                'status': 'pass' if validation_result['valid'] else 'fail',
                'metadata': metadata,
                'validation': validation_result,
                'errors': validation_result.get('errors', [])
            }
            
            logger.info(f"Technical check completed. Status: {result['status']}")
            return result
            
        except Exception as e:
            logger.error(f"Technical check failed: {e}")
            return {
                'status': 'fail',
                'metadata': {},
                'validation': {'valid': False},
                'errors': [f'Technical analysis failed: {str(e)}']
            }
    
    def _extract_metadata(self, video_path):
        """
        Extract video metadata using FFprobe
        
        Args:
            video_path (str): Path to the video file
            
        Returns:
            dict: Video metadata
        """
        try:
            # FFprobe command to extract JSON metadata
            cmd = [
                'ffprobe',
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_format',
                '-show_streams',
                video_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            metadata = json.loads(result.stdout)
            
            # Extract video stream information
            video_stream = None
            for stream in metadata.get('streams', []):
                if stream.get('codec_type') == 'video':
                    video_stream = stream
                    break
            
            if not video_stream:
                raise Exception("No video stream found in file")
            
            # Parse metadata into standardized format
            parsed_metadata = {
                'width': int(video_stream.get('width', 0)),
                'height': int(video_stream.get('height', 0)),
                'codec_name': video_stream.get('codec_name', '').lower(),
                'codec_long_name': video_stream.get('codec_long_name', ''),
                'frame_rate': self._parse_frame_rate(video_stream.get('r_frame_rate', '0/1')),
                'avg_frame_rate': self._parse_frame_rate(video_stream.get('avg_frame_rate', '0/1')),
                'duration': float(video_stream.get('duration', 0)),
                'bit_rate': int(video_stream.get('bit_rate', 0)),
                'profile': video_stream.get('profile', ''),
                'level': video_stream.get('level', ''),
                'pixel_format': video_stream.get('pix_fmt', ''),
                'file_size': int(metadata.get('format', {}).get('size', 0)),
                'format_name': metadata.get('format', {}).get('format_name', '')
            }
            
            return parsed_metadata
            
        except subprocess.CalledProcessError as e:
            logger.error(f"FFprobe command failed: {e}")
            raise Exception(f"Failed to extract video metadata: {e}")
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse FFprobe output: {e}")
            raise Exception(f"Invalid metadata format: {e}")
        except Exception as e:
            logger.error(f"Metadata extraction error: {e}")
            raise
    
    def _parse_frame_rate(self, frame_rate_str):
        """
        Parse frame rate from FFprobe format (e.g., "30000/1001")
        
        Args:
            frame_rate_str (str): Frame rate in fraction format
            
        Returns:
            float: Frame rate as decimal
        """
        try:
            if '/' in frame_rate_str:
                numerator, denominator = frame_rate_str.split('/')
                return float(numerator) / float(denominator)
            else:
                return float(frame_rate_str)
        except (ValueError, ZeroDivisionError):
            return 0.0
    
    def _validate_metadata(self, metadata):
        """
        Validate video metadata against quality standards
        
        Args:
            metadata (dict): Video metadata
            
        Returns:
            dict: Validation results
        """
        errors = []
        warnings = []
        
        # Check resolution
        width = metadata.get('width', 0)
        height = metadata.get('height', 0)
        min_width, min_height = self.required_standards['min_resolution']
        
        if width < min_width or height < min_height:
            errors.append(f"Resolution {width}x{height} is below minimum requirement of {min_width}x{min_height}")
        
        # Check frame rate
        frame_rate = metadata.get('frame_rate', 0)
        valid_frame_rates = self.required_standards['valid_frame_rates']
        
        # Allow small tolerance for frame rate comparison (0.1 fps)
        frame_rate_valid = any(abs(frame_rate - valid_rate) < 0.1 for valid_rate in valid_frame_rates)
        
        if not frame_rate_valid:
            errors.append(f"Frame rate {frame_rate:.3f} FPS is not in approved list: {valid_frame_rates}")
        
        # Check codec
        codec_name = metadata.get('codec_name', '').lower()
        valid_codecs = self.required_standards['valid_codecs']
        
        codec_valid = any(valid_codec in codec_name for valid_codec in valid_codecs)
        
        if not codec_valid:
            errors.append(f"Codec '{codec_name}' is not in approved list: {valid_codecs}")
        
        # Additional quality checks
        bit_rate = metadata.get('bit_rate', 0)
        if bit_rate > 0 and bit_rate < 1000000:  # Less than 1 Mbps
            warnings.append(f"Low bit rate detected: {bit_rate / 1000000:.2f} Mbps")
        
        duration = metadata.get('duration', 0)
        if duration <= 0:
            warnings.append("Could not determine video duration")
        
        # Determine overall validity
        is_valid = len(errors) == 0
        
        return {
            'valid': is_valid,
            'errors': errors,
            'warnings': warnings,
            'resolution_check': {
                'current': f"{width}x{height}",
                'required': f"{min_width}x{min_height}",
                'pass': width >= min_width and height >= min_height
            },
            'frame_rate_check': {
                'current': round(frame_rate, 3),
                'valid_rates': valid_frame_rates,
                'pass': frame_rate_valid
            },
            'codec_check': {
                'current': codec_name,
                'valid_codecs': valid_codecs,
                'pass': codec_valid
            }
        }
