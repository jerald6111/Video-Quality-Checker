import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

class ApiService {
  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 300000, // 5 minutes timeout for video processing
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  /**
   * Check if the API is healthy
   * @returns {Promise} API health status
   */
  async checkHealth() {
    try {
      const response = await this.client.get('/api/health');
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  /**
   * Submit video quality check request
   * @param {string} iconikUrl - The Iconik share URL
   * @param {Array} customVocabulary - Custom vocabulary words
   * @returns {Promise} Quality check results
   */
  async checkVideoQuality(iconikUrl, customVocabulary = []) {
    try {
      const requestData = {
        url: iconikUrl,
        vocabulary: customVocabulary,
      };

      const response = await this.client.post('/api/check_quality', requestData);
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  /**
   * Handle API errors and format them consistently
   * @param {Error} error - The error object
   * @returns {Object} Formatted error object
   */
  handleError(error) {
    if (error.response) {
      // Server responded with error status
      return {
        message: error.response.data?.error || 'Server error occurred',
        status: error.response.status,
        details: error.response.data,
      };
    } else if (error.request) {
      // Request was made but no response received
      return {
        message: 'No response from server. Please check your connection.',
        status: 0,
        details: null,
      };
    } else {
      // Something else happened
      return {
        message: error.message || 'An unexpected error occurred',
        status: -1,
        details: null,
      };
    }
  }
}

export default new ApiService();
