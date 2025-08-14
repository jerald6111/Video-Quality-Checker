import React, { useState, useEffect } from 'react';
import VideoUrlForm from './components/VideoUrlForm';
import ResultsDisplay from './components/ResultsDisplay';
import ApiService from './services/api';
import { AlertCircle, CheckCircle, Video } from 'lucide-react';
import './App.css';

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [apiHealth, setApiHealth] = useState(null);

  useEffect(() => {
    // Check API health on component mount
    checkApiHealth();
  }, []);

  const checkApiHealth = async () => {
    try {
      const health = await ApiService.checkHealth();
      setApiHealth(health);
    } catch (err) {
      setApiHealth({ status: 'unhealthy', error: err.message });
    }
  };

  const handleVideoCheck = async (iconikUrl, customVocabulary) => {
    setIsLoading(true);
    setError(null);
    setResults(null);

    try {
      const response = await ApiService.checkVideoQuality(iconikUrl, customVocabulary);
      setResults(response);
    } catch (err) {
      setError(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <Video className="text-blue-600 mr-3" size={32} />
              <div>
                <h1 className="text-2xl font-bold text-gray-900">
                  Video Quality Checker
                </h1>
                <p className="text-sm text-gray-600">
                  Advanced quality analysis for Iconik video links
                </p>
              </div>
            </div>
            
            {/* API Health Indicator */}
            <div className="flex items-center">
              {apiHealth?.status === 'healthy' ? (
                <div className="flex items-center text-green-600">
                  <CheckCircle size={20} className="mr-1" />
                  <span className="text-sm font-medium">API Online</span>
                </div>
              ) : (
                <div className="flex items-center text-red-600">
                  <AlertCircle size={20} className="mr-1" />
                  <span className="text-sm font-medium">API Offline</span>
                </div>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Instructions */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-6">
          <h2 className="text-lg font-semibold text-blue-800 mb-3">How it works:</h2>
          <ol className="list-decimal list-inside space-y-2 text-blue-700">
            <li>Paste your Iconik share URL in the form below</li>
            <li>Optionally add custom vocabulary to prevent false spelling errors</li>
            <li>Click "Check Quality" to start the analysis</li>
            <li>Wait for the comprehensive technical and content quality report</li>
          </ol>
          
          <div className="mt-4 p-4 bg-white rounded border border-blue-200">
            <h3 className="font-medium text-blue-800 mb-2">Quality Standards:</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-blue-700">
              <div>
                <strong>Resolution:</strong> 1920x1080 minimum
              </div>
              <div>
                <strong>Frame Rate:</strong> 23.976, 24, 25, 29.97, 30, 50, 60 FPS
              </div>
              <div>
                <strong>Codec:</strong> H.264 or ProRes
              </div>
            </div>
          </div>
        </div>

        {/* Form */}
        <VideoUrlForm 
          onSubmit={handleVideoCheck} 
          isLoading={isLoading} 
        />

        {/* Results */}
        <ResultsDisplay 
          results={results} 
          error={error} 
        />

        {/* Loading State */}
        {isLoading && (
          <div className="bg-white rounded-lg shadow-md p-8 text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <h3 className="text-lg font-semibold text-gray-700 mb-2">
              Processing Video...
            </h3>
            <p className="text-gray-600">
              This may take several minutes depending on video size and content complexity.
            </p>
            <div className="mt-4 bg-gray-100 rounded-lg p-4">
              <div className="text-sm text-gray-600 space-y-1">
                <div>⬇️ Downloading video from Iconik</div>
                <div>🔍 Analyzing technical specifications</div>
                <div>📝 Extracting and checking text content</div>
                <div>📊 Generating comprehensive report</div>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="text-center text-gray-600">
            <p className="text-sm">
              Video Quality & Content Checker | Built for Iconik video analysis
            </p>
            <p className="text-xs mt-1">
              Supports technical quality validation and OCR-based content checking
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
