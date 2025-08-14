import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import tempfile
import logging

logger = logging.getLogger(__name__)

class VideoDownloader:
    """Service for downloading videos from Iconik share links"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def download_from_iconik(self, iconik_url, download_dir):
        """
        Download video from Iconik share URL
        
        Args:
            iconik_url (str): The Iconik share URL
            download_dir (str): Directory to save the downloaded video
            
        Returns:
            str: Path to the downloaded video file
        """
        try:
            logger.info(f"Fetching Iconik page: {iconik_url}")
            
            # Get the Iconik share page
            response = self.session.get(iconik_url, timeout=30)
            response.raise_for_status()
            
            # Parse the HTML to find the video download link
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for common video download patterns in Iconik
            download_url = self._extract_download_url(soup, iconik_url)
            
            if not download_url:
                raise Exception("Could not find video download URL in Iconik page")
            
            logger.info(f"Found download URL: {download_url}")
            
            # Download the video file
            return self._download_video_file(download_url, download_dir)
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error downloading from Iconik: {e}")
            raise Exception(f"Failed to access Iconik URL: {e}")
        except Exception as e:
            logger.error(f"Error downloading video: {e}")
            raise
    
    def _extract_download_url(self, soup, base_url):
        """
        Extract the direct video download URL from Iconik page HTML
        
        Args:
            soup (BeautifulSoup): Parsed HTML content
            base_url (str): Base URL for resolving relative links
            
        Returns:
            str: Direct download URL for the video
        """
        # Strategy 1: Look for download buttons or links
        download_selectors = [
            'a[href*="download"]',
            'a[href*=".mp4"]',
            'a[href*=".mov"]',
            'a[href*=".avi"]',
            'button[data-url]',
            '[data-download-url]'
        ]
        
        for selector in download_selectors:
            elements = soup.select(selector)
            for element in elements:
                href = element.get('href') or element.get('data-url') or element.get('data-download-url')
                if href:
                    # Convert relative URLs to absolute
                    full_url = urljoin(base_url, href)
                    if self._is_video_url(full_url):
                        return full_url
        
        # Strategy 2: Look for video tags with src attributes
        video_tags = soup.find_all('video')
        for video in video_tags:
            src = video.get('src')
            if src:
                full_url = urljoin(base_url, src)
                if self._is_video_url(full_url):
                    return full_url
            
            # Check source tags within video
            sources = video.find_all('source')
            for source in sources:
                src = source.get('src')
                if src:
                    full_url = urljoin(base_url, src)
                    if self._is_video_url(full_url):
                        return full_url
        
        # Strategy 3: Look for API endpoints or data attributes
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string:
                # Look for URLs in JavaScript that might contain video links
                lines = script.string.split('\n')
                for line in lines:
                    if any(ext in line for ext in ['.mp4', '.mov', '.avi', 'download']):
                        # Extract potential URLs from the line
                        import re
                        urls = re.findall(r'https?://[^\s"\'>]+', line)
                        for url in urls:
                            if self._is_video_url(url):
                                return url
        
        return None
    
    def _is_video_url(self, url):
        """
        Check if URL likely points to a video file
        
        Args:
            url (str): URL to check
            
        Returns:
            bool: True if URL likely contains a video
        """
        video_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv', '.webm']
        url_lower = url.lower()
        
        # Check file extension
        for ext in video_extensions:
            if ext in url_lower:
                return True
        
        # Check for common video hosting patterns
        video_patterns = ['download', 'stream', 'media', 'video']
        for pattern in video_patterns:
            if pattern in url_lower:
                return True
        
        return False
    
    def _download_video_file(self, download_url, download_dir):
        """
        Download the actual video file
        
        Args:
            download_url (str): Direct URL to the video file
            download_dir (str): Directory to save the file
            
        Returns:
            str: Path to the downloaded file
        """
        try:
            logger.info(f"Downloading video from: {download_url}")
            
            # Make HEAD request to get file info
            head_response = self.session.head(download_url, timeout=30)
            head_response.raise_for_status()
            
            # Get filename from URL or Content-Disposition header
            filename = self._get_filename(download_url, head_response.headers)
            file_path = os.path.join(download_dir, filename)
            
            # Download the file
            response = self.session.get(download_url, stream=True, timeout=60)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded_size = 0
            
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        
                        # Log progress for large files
                        if total_size > 0 and downloaded_size % (1024 * 1024 * 10) == 0:  # Every 10MB
                            progress = (downloaded_size / total_size) * 100
                            logger.info(f"Download progress: {progress:.1f}%")
            
            logger.info(f"Video downloaded successfully: {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"Error downloading video file: {e}")
            raise
    
    def _get_filename(self, url, headers):
        """
        Extract filename from URL or headers
        
        Args:
            url (str): Download URL
            headers (dict): Response headers
            
        Returns:
            str: Filename for the downloaded file
        """
        # Try to get filename from Content-Disposition header
        content_disposition = headers.get('content-disposition', '')
        if 'filename=' in content_disposition:
            import re
            match = re.search(r'filename[^;=\n]*=(([\'"]).*?\2|[^;\n]*)', content_disposition)
            if match:
                filename = match.groups()[0].strip('"\'')
                if filename:
                    return filename
        
        # Extract filename from URL
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        
        # If no extension, add .mp4 as default
        if not os.path.splitext(filename)[1]:
            filename += '.mp4'
        
        # If no filename, generate one
        if not filename or filename == '.mp4':
            filename = f'video_{os.urandom(4).hex()}.mp4'
        
        return filename
