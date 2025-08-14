import React from 'react';
import { 
  CheckCircle, 
  XCircle, 
  AlertTriangle, 
  Clock, 
  FileVideo, 
  Type,
  Monitor,
  Zap,
  HardDrive
} from 'lucide-react';

const ResultsDisplay = ({ results, error }) => {
  if (error) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex items-center text-red-600 mb-4">
          <XCircle className="mr-2" size={24} />
          <h3 className="text-xl font-bold">Error</h3>
        </div>
        <p className="text-gray-700">{error.message}</p>
        {error.details && (
          <div className="mt-4 p-3 bg-red-50 rounded-md">
            <p className="text-sm text-red-800">
              Status: {error.status} | Details: {JSON.stringify(error.details, null, 2)}
            </p>
          </div>
        )}
      </div>
    );
  }

  if (!results) {
    return null;
  }

  const getStatusIcon = (status) => {
    switch (status) {
      case 'pass':
        return <CheckCircle className="text-green-600" size={24} />;
      case 'fail':
        return <XCircle className="text-red-600" size={24} />;
      default:
        return <AlertTriangle className="text-yellow-600" size={24} />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'pass':
        return 'text-green-600 bg-green-50 border-green-200';
      case 'fail':
        return 'text-red-600 bg-red-50 border-red-200';
      default:
        return 'text-yellow-600 bg-yellow-50 border-yellow-200';
    }
  };

  return (
    <div className="space-y-6">
      {/* Overall Status */}
      <div className={`border rounded-lg p-6 ${getStatusColor(results.status)}`}>
        <div className="flex items-center mb-4">
          {getStatusIcon(results.status)}
          <h3 className="text-2xl font-bold ml-2">
            Overall Status: {results.status.charAt(0).toUpperCase() + results.status.slice(1)}
          </h3>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="flex items-center">
            <Monitor className="mr-2" size={20} />
            <span>Technical Quality: </span>
            <span className={`ml-1 font-semibold ${
              results.technical_status === 'pass' ? 'text-green-700' : 'text-red-700'
            }`}>
              {results.technical_status.charAt(0).toUpperCase() + results.technical_status.slice(1)}
            </span>
          </div>
          
          <div className="flex items-center">
            <Type className="mr-2" size={20} />
            <span>Content Quality: </span>
            <span className={`ml-1 font-semibold ${
              results.content_status === 'pass' ? 'text-green-700' : 'text-red-700'
            }`}>
              {results.content_status.charAt(0).toUpperCase() + results.content_status.slice(1)}
            </span>
          </div>
        </div>

        {results.timestamp && (
          <div className="mt-4 flex items-center text-sm opacity-75">
            <Clock className="mr-1" size={16} />
            <span>Checked on: {new Date(results.timestamp).toLocaleString()}</span>
          </div>
        )}
      </div>

      {/* Technical Metadata */}
      {results.technical_metadata && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h4 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
            <FileVideo className="mr-2" size={20} />
            Technical Metadata
          </h4>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div className="bg-gray-50 p-3 rounded-md">
              <div className="flex items-center mb-1">
                <Monitor className="mr-2 text-blue-600" size={16} />
                <span className="font-medium">Resolution</span>
              </div>
              <span className="text-lg">{results.technical_metadata.resolution}</span>
            </div>
            
            <div className="bg-gray-50 p-3 rounded-md">
              <div className="flex items-center mb-1">
                <Zap className="mr-2 text-green-600" size={16} />
                <span className="font-medium">Frame Rate</span>
              </div>
              <span className="text-lg">{results.technical_metadata.frame_rate} FPS</span>
            </div>
            
            <div className="bg-gray-50 p-3 rounded-md">
              <div className="flex items-center mb-1">
                <FileVideo className="mr-2 text-purple-600" size={16} />
                <span className="font-medium">Codec</span>
              </div>
              <span className="text-lg">{results.technical_metadata.codec}</span>
            </div>
            
            <div className="bg-gray-50 p-3 rounded-md">
              <div className="flex items-center mb-1">
                <Clock className="mr-2 text-orange-600" size={16} />
                <span className="font-medium">Duration</span>
              </div>
              <span className="text-lg">{results.technical_metadata.duration}s</span>
            </div>
            
            <div className="bg-gray-50 p-3 rounded-md">
              <div className="flex items-center mb-1">
                <Zap className="mr-2 text-red-600" size={16} />
                <span className="font-medium">Bit Rate</span>
              </div>
              <span className="text-lg">{results.technical_metadata.bit_rate}</span>
            </div>
            
            <div className="bg-gray-50 p-3 rounded-md">
              <div className="flex items-center mb-1">
                <HardDrive className="mr-2 text-gray-600" size={16} />
                <span className="font-medium">File Size</span>
              </div>
              <span className="text-lg">{results.technical_metadata.file_size}</span>
            </div>
          </div>
        </div>
      )}

      {/* Content Analysis */}
      {results.content_analysis && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h4 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
            <Type className="mr-2" size={20} />
            Content Analysis
          </h4>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="bg-gray-50 p-3 rounded-md">
              <span className="font-medium block">Text Detected</span>
              <span className={`text-lg ${results.content_analysis.text_detected ? 'text-green-600' : 'text-gray-500'}`}>
                {results.content_analysis.text_detected ? 'Yes' : 'No'}
              </span>
            </div>
            
            <div className="bg-gray-50 p-3 rounded-md">
              <span className="font-medium block">Frames Analyzed</span>
              <span className="text-lg">{results.content_analysis.total_keyframes_analyzed}</span>
            </div>
            
            <div className="bg-gray-50 p-3 rounded-md">
              <span className="font-medium block">Spelling Errors</span>
              <span className={`text-lg ${results.content_analysis.spelling_errors > 0 ? 'text-red-600' : 'text-green-600'}`}>
                {results.content_analysis.spelling_errors}
              </span>
            </div>
            
            <div className="bg-gray-50 p-3 rounded-md">
              <span className="font-medium block">Grammar Issues</span>
              <span className={`text-lg ${results.content_analysis.grammar_errors > 0 ? 'text-red-600' : 'text-green-600'}`}>
                {results.content_analysis.grammar_errors}
              </span>
            </div>
          </div>
        </div>
      )}

      {/* Errors */}
      {results.errors && results.errors.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h4 className="text-xl font-bold text-red-600 mb-4 flex items-center">
            <AlertTriangle className="mr-2" size={20} />
            Issues Found ({results.errors.length})
          </h4>
          
          <div className="space-y-3">
            {results.errors.map((error, index) => (
              <div key={index} className="border-l-4 border-red-500 bg-red-50 p-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="font-medium text-red-800 capitalize">
                    {error.type} Error
                  </span>
                  {error.timestamp && error.timestamp !== 'N/A' && (
                    <span className="text-sm text-red-600 flex items-center">
                      <Clock className="mr-1" size={14} />
                      {error.timestamp}
                    </span>
                  )}
                </div>
                
                {error.word && (
                  <div className="mb-1">
                    <span className="text-red-700">Word: </span>
                    <span className="font-mono bg-red-100 px-2 py-1 rounded text-red-800">
                      {error.word}
                    </span>
                  </div>
                )}
                
                {error.suggestion && (
                  <div className="mb-1">
                    <span className="text-red-700">Suggestion: </span>
                    <span className="text-red-800">{error.suggestion}</span>
                  </div>
                )}
                
                {error.error && (
                  <div className="text-red-800">{error.error}</div>
                )}
                
                {error.context && (
                  <div className="mt-2 text-sm text-red-600">
                    <span className="font-medium">Context: </span>
                    <span className="italic">"{error.context}"</span>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Recommendations */}
      {results.recommendations && results.recommendations.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h4 className="text-xl font-bold text-blue-600 mb-4 flex items-center">
            <AlertTriangle className="mr-2" size={20} />
            Recommendations
          </h4>
          
          <div className="space-y-3">
            {results.recommendations.map((rec, index) => (
              <div key={index} className="border-l-4 border-blue-500 bg-blue-50 p-4">
                <div className="font-medium text-blue-800 mb-1 capitalize">
                  {rec.category}: {rec.issue}
                </div>
                <div className="text-blue-700">{rec.recommendation}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Summary */}
      {results.summary && (
        <div className="bg-gray-50 rounded-lg p-4">
          <h5 className="font-bold text-gray-800 mb-2">Summary</h5>
          <div className="text-sm text-gray-600 space-y-1">
            <div>Total Issues: {results.summary.total_errors}</div>
            <div>Technical Issues: {results.summary.technical_errors}</div>
            <div>Content Issues: {results.summary.content_errors}</div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ResultsDisplay;
