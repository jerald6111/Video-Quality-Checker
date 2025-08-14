import React, { useState } from 'react';
import { Link, Upload, Clock, AlertCircle, CheckCircle } from 'lucide-react';

const VideoUrlForm = ({ onSubmit, isLoading }) => {
  const [iconikUrl, setIconikUrl] = useState('');
  const [customVocabulary, setCustomVocabulary] = useState('');
  const [errors, setErrors] = useState({});

  const validateForm = () => {
    const newErrors = {};

    if (!iconikUrl.trim()) {
      newErrors.url = 'Iconik URL is required';
    } else if (!iconikUrl.toLowerCase().includes('iconik')) {
      newErrors.url = 'Please enter a valid Iconik share URL';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    const vocabularyArray = customVocabulary
      .split(',')
      .map(word => word.trim())
      .filter(word => word.length > 0);

    onSubmit(iconikUrl.trim(), vocabularyArray);
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 mb-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-4 flex items-center">
        <Upload className="mr-2" size={24} />
        Video Quality Check
      </h2>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="iconik-url" className="block text-sm font-medium text-gray-700 mb-1">
            Iconik Share URL *
          </label>
          <div className="relative">
            <Link className="absolute left-3 top-3 text-gray-400" size={20} />
            <input
              id="iconik-url"
              type="url"
              value={iconikUrl}
              onChange={(e) => setIconikUrl(e.target.value)}
              placeholder="https://app.iconik.io/..."
              className={`w-full pl-10 pr-4 py-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                errors.url ? 'border-red-500' : 'border-gray-300'
              }`}
              disabled={isLoading}
            />
          </div>
          {errors.url && (
            <p className="mt-1 text-sm text-red-600 flex items-center">
              <AlertCircle size={16} className="mr-1" />
              {errors.url}
            </p>
          )}
        </div>

        <div>
          <label htmlFor="custom-vocabulary" className="block text-sm font-medium text-gray-700 mb-1">
            Custom Vocabulary (Optional)
          </label>
          <textarea
            id="custom-vocabulary"
            value={customVocabulary}
            onChange={(e) => setCustomVocabulary(e.target.value)}
            placeholder="Enter custom words separated by commas (e.g., Iconik, ProRes, H.264)"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            rows={3}
            disabled={isLoading}
          />
          <p className="mt-1 text-sm text-gray-500">
            Add specific terms or names to prevent false spelling errors
          </p>
        </div>

        <button
          type="submit"
          disabled={isLoading}
          className={`w-full py-3 px-4 rounded-md text-white font-medium transition-colors ${
            isLoading
              ? 'bg-gray-400 cursor-not-allowed'
              : 'bg-blue-600 hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2'
          }`}
        >
          {isLoading ? (
            <span className="flex items-center justify-center">
              <Clock className="animate-spin mr-2" size={20} />
              Checking Video Quality...
            </span>
          ) : (
            'Check Quality'
          )}
        </button>
      </form>
    </div>
  );
};

export default VideoUrlForm;
