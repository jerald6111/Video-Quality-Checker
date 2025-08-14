import logging

logger = logging.getLogger(__name__)

class ReportGenerator:
    """Service for generating comprehensive quality check reports"""
    
    def __init__(self):
        pass
    
    def generate_report(self, technical_result, content_result):
        """
        Generate comprehensive quality check report
        
        Args:
            technical_result (dict): Results from technical quality check
            content_result (dict): Results from content quality check
            
        Returns:
            dict: Complete quality check report
        """
        try:
            logger.info("Generating comprehensive quality report")
            
            # Determine overall status
            technical_status = technical_result.get('status', 'fail')
            content_status = content_result.get('status', 'fail')
            overall_status = 'pass' if technical_status == 'pass' and content_status == 'pass' else 'fail'
            
            # Combine all errors
            all_errors = []
            
            # Add technical errors
            technical_errors = technical_result.get('errors', [])
            for error in technical_errors:
                all_errors.append({
                    'type': 'technical',
                    'error': error,
                    'timestamp': 'N/A'
                })
            
            # Add content errors
            content_errors = content_result.get('errors', [])
            all_errors.extend(content_errors)
            
            # Build technical metadata summary
            technical_metadata = self._build_technical_metadata(technical_result)
            
            # Build content analysis summary
            content_analysis = self._build_content_analysis(content_result)
            
            # Create comprehensive report
            report = {
                'status': overall_status,
                'technical_status': technical_status,
                'content_status': content_status,
                'timestamp': self._get_current_timestamp(),
                'technical_metadata': technical_metadata,
                'content_analysis': content_analysis,
                'errors': all_errors,
                'summary': {
                    'total_errors': len(all_errors),
                    'technical_errors': len(technical_errors),
                    'content_errors': len(content_errors),
                    'technical_passed': technical_status == 'pass',
                    'content_passed': content_status == 'pass'
                }
            }
            
            # Add recommendations if there are errors
            if all_errors:
                report['recommendations'] = self._generate_recommendations(technical_result, content_result)
            
            logger.info(f"Report generated successfully. Overall status: {overall_status}")
            return report
            
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            return {
                'status': 'fail',
                'technical_status': 'fail',
                'content_status': 'fail',
                'errors': [f'Report generation failed: {str(e)}'],
                'timestamp': self._get_current_timestamp()
            }
    
    def _build_technical_metadata(self, technical_result):
        """
        Build technical metadata summary
        
        Args:
            technical_result (dict): Technical check results
            
        Returns:
            dict: Technical metadata summary
        """
        metadata = technical_result.get('metadata', {})
        validation = technical_result.get('validation', {})
        
        return {
            'resolution': f"{metadata.get('width', 0)}x{metadata.get('height', 0)}",
            'frame_rate': round(metadata.get('frame_rate', 0), 3),
            'codec': metadata.get('codec_name', 'Unknown'),
            'codec_profile': metadata.get('profile', 'Unknown'),
            'duration': round(metadata.get('duration', 0), 2),
            'bit_rate': self._format_bit_rate(metadata.get('bit_rate', 0)),
            'file_size': self._format_file_size(metadata.get('file_size', 0)),
            'pixel_format': metadata.get('pixel_format', 'Unknown'),
            'format': metadata.get('format_name', 'Unknown'),
            'validation_details': {
                'resolution_check': validation.get('resolution_check', {}),
                'frame_rate_check': validation.get('frame_rate_check', {}),
                'codec_check': validation.get('codec_check', {})
            }
        }
    
    def _build_content_analysis(self, content_result):
        """
        Build content analysis summary
        
        Args:
            content_result (dict): Content check results
            
        Returns:
            dict: Content analysis summary
        """
        return {
            'text_detected': content_result.get('text_found', False),
            'total_keyframes_analyzed': content_result.get('total_keyframes', 0),
            'frames_with_text': content_result.get('extracted_text_count', 0),
            'spelling_errors': len([e for e in content_result.get('errors', []) if e.get('type') == 'spelling']),
            'grammar_errors': len([e for e in content_result.get('errors', []) if e.get('type') == 'grammar']),
            'warnings': content_result.get('warnings', [])
        }
    
    def _generate_recommendations(self, technical_result, content_result):
        """
        Generate recommendations based on found issues
        
        Args:
            technical_result (dict): Technical check results
            content_result (dict): Content check results
            
        Returns:
            list: List of recommendations
        """
        recommendations = []
        
        # Technical recommendations
        if technical_result.get('status') == 'fail':
            validation = technical_result.get('validation', {})
            
            if not validation.get('resolution_check', {}).get('pass', True):
                recommendations.append({
                    'category': 'technical',
                    'issue': 'Resolution too low',
                    'recommendation': 'Ensure video resolution is at least 1920x1080 (1080p)'
                })
            
            if not validation.get('frame_rate_check', {}).get('pass', True):
                recommendations.append({
                    'category': 'technical',
                    'issue': 'Invalid frame rate',
                    'recommendation': 'Use standard frame rates: 23.976, 24, 25, 29.97, 30, 50, or 60 FPS'
                })
            
            if not validation.get('codec_check', {}).get('pass', True):
                recommendations.append({
                    'category': 'technical',
                    'issue': 'Unsupported codec',
                    'recommendation': 'Encode video using H.264 or ProRes codec'
                })
        
        # Content recommendations
        if content_result.get('status') == 'fail':
            content_errors = content_result.get('errors', [])
            spelling_errors = [e for e in content_errors if e.get('type') == 'spelling']
            grammar_errors = [e for e in content_errors if e.get('type') == 'grammar']
            
            if spelling_errors:
                recommendations.append({
                    'category': 'content',
                    'issue': f'{len(spelling_errors)} spelling error(s) found',
                    'recommendation': 'Review and correct spelling errors in video text content'
                })
            
            if grammar_errors:
                recommendations.append({
                    'category': 'content',
                    'issue': f'{len(grammar_errors)} grammar issue(s) found',
                    'recommendation': 'Review and correct grammar issues in video text content'
                })
        
        return recommendations
    
    def _format_bit_rate(self, bit_rate):
        """
        Format bit rate in human-readable format
        
        Args:
            bit_rate (int): Bit rate in bits per second
            
        Returns:
            str: Formatted bit rate
        """
        if bit_rate == 0:
            return 'Unknown'
        
        # Convert to Mbps
        mbps = bit_rate / 1000000
        return f"{mbps:.2f} Mbps"
    
    def _format_file_size(self, file_size):
        """
        Format file size in human-readable format
        
        Args:
            file_size (int): File size in bytes
            
        Returns:
            str: Formatted file size
        """
        if file_size == 0:
            return 'Unknown'
        
        # Convert to appropriate unit
        for unit in ['B', 'KB', 'MB', 'GB']:
            if file_size < 1024.0:
                return f"{file_size:.2f} {unit}"
            file_size /= 1024.0
        
        return f"{file_size:.2f} TB"
    
    def _get_current_timestamp(self):
        """
        Get current timestamp in ISO format
        
        Returns:
            str: Current timestamp
        """
        from datetime import datetime
        return datetime.now().isoformat()
