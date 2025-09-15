import React, { useState, useRef, useCallback } from 'react';
import { Upload, Download, Zap, AlertCircle, CheckCircle, Loader } from 'lucide-react';
import { faceSwap } from '../services/api';

const FaceSwap = () => {
  const [sourceImage, setSourceImage] = useState(null);
  const [targetImage, setTargetImage] = useState(null);
  const [result, setResult] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState(null);
  const [dragActive, setDragActive] = useState({ source: false, target: false });
  
  const sourceInputRef = useRef(null);
  const targetInputRef = useRef(null);

  const handleDrag = useCallback((e, type) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(prev => ({ ...prev, [type]: true }));
    } else if (e.type === "dragleave") {
      setDragActive(prev => ({ ...prev, [type]: false }));
    }
  }, []);

  const handleDrop = useCallback((e, type) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(prev => ({ ...prev, [type]: false }));
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileUpload(e.dataTransfer.files[0], type);
    }
  }, []);

  const handleFileUpload = (file, type) => {
    if (!file.type.startsWith('image/')) {
      setError('Please upload a valid image file');
      return;
    }

    const reader = new FileReader();
    reader.onload = (e) => {
      if (type === 'source') {
        setSourceImage({ file, preview: e.target.result });
      } else {
        setTargetImage({ file, preview: e.target.result });
      }
      setError(null);
      setResult(null);
    };
    reader.readAsDataURL(file);
  };

  const handleInputChange = (e, type) => {
    const file = e.target.files[0];
    if (file) {
      handleFileUpload(file, type);
    }
  };

  const handleSubmit = async () => {
    if (!sourceImage || !targetImage) {
      setError('Please upload both source and target images');
      return;
    }

    setIsProcessing(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('source_image', sourceImage.file);
      formData.append('target_image', targetImage.file);

      const response = await faceSwap(formData);
      
      if (response.success) {
        setResult(response);
      } else {
        setError(response.error || 'Face swap failed');
      }
    } catch (err) {
      setError(err.message || 'An error occurred during processing');
    } finally {
      setIsProcessing(false);
    }
  };

  const downloadResult = () => {
    if (result && result.result_url) {
      const link = document.createElement('a');
      link.href = result.result_url;
      link.download = 'face-swap-result.jpg';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  };

  const reset = () => {
    setSourceImage(null);
    setTargetImage(null);
    setResult(null);
    setError(null);
    setIsProcessing(false);
  };

  const UploadArea = ({ type, image, dragActive: isDragActive, onDrop, onDrag, inputRef, onChange }) => (
    <div
      className={`relative border-2 border-dashed rounded-lg p-6 text-center transition-all duration-300 ${
        isDragActive
          ? 'border-blue-500 bg-blue-50'
          : image
          ? 'border-green-500 bg-green-50'
          : 'border-gray-300 hover:border-gray-400'
      }`}
      onDragEnter={(e) => onDrag(e, type)}
      onDragLeave={(e) => onDrag(e, type)}
      onDragOver={(e) => onDrag(e, type)}
      onDrop={(e) => onDrop(e, type)}
    >
      {image ? (
        <div className="space-y-4">
          <img
            src={image.preview}
            alt={`${type} preview`}
            className="w-full h-48 object-cover rounded-lg shadow-md"
          />
          <div className="flex items-center justify-center text-green-600">
            <CheckCircle className="w-5 h-5 mr-2" />
            <span className="font-medium">{type === 'source' ? 'Source' : 'Target'} image uploaded</span>
          </div>
          <button
            type="button"
            onClick={() => inputRef.current?.click()}
            className="text-blue-600 hover:text-blue-700 font-medium"
          >
            Change image
          </button>
        </div>
      ) : (
        <div className="space-y-4">
          <Upload className="w-12 h-12 text-gray-400 mx-auto" />
          <div>
            <p className="text-lg font-medium text-gray-700">
              Upload {type === 'source' ? 'Source' : 'Target'} Image
            </p>
            <p className="text-gray-500 mt-1">
              {type === 'source' 
                ? 'The face you want to use'
                : 'The image where you want to place the face'
              }
            </p>
          </div>
          <button
            type="button"
            onClick={() => inputRef.current?.click()}
            className="inline-flex items-center px-4 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors"
          >
            <Upload className="w-4 h-4 mr-2" />
            Choose File
          </button>
          <p className="text-sm text-gray-400">
            or drag and drop an image here
          </p>
        </div>
      )}
      <input
        ref={inputRef}
        type="file"
        className="hidden"
        accept="image/*"
        onChange={(e) => onChange(e, type)}
      />
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            AI Face Swap
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Upload two images and let our AI seamlessly swap faces with professional quality results
          </p>
        </div>

        {/* Error Alert */}
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-center">
            <AlertCircle className="w-5 h-5 text-red-500 mr-3 flex-shrink-0" />
            <span className="text-red-700">{error}</span>
          </div>
        )}

        {/* Upload Section */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Source Image</h3>
            <UploadArea
              type="source"
              image={sourceImage}
              dragActive={dragActive.source}
              onDrop={handleDrop}
              onDrag={handleDrag}
              inputRef={sourceInputRef}
              onChange={handleInputChange}
            />
          </div>
          
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Target Image</h3>
            <UploadArea
              type="target"
              image={targetImage}
              dragActive={dragActive.target}
              onDrop={handleDrop}
              onDrag={handleDrag}
              inputRef={targetInputRef}
              onChange={handleInputChange}
            />
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center mb-8">
          <button
            onClick={handleSubmit}
            disabled={!sourceImage || !targetImage || isProcessing}
            className="inline-flex items-center px-8 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-semibold rounded-lg hover:from-blue-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
          >
            {isProcessing ? (
              <Loader className="w-5 h-5 mr-2 animate-spin" />
            ) : (
              <Zap className="w-5 h-5 mr-2" />
            )}
            {isProcessing ? 'Processing...' : 'Swap Faces'}
          </button>
          
          <button
            onClick={reset}
            className="inline-flex items-center px-8 py-3 border border-gray-300 text-gray-700 font-semibold rounded-lg hover:bg-gray-50 transition-colors"
          >
            Reset
          </button>
        </div>

        {/* Processing Status */}
        {isProcessing && (
          <div className="mb-8 p-6 bg-blue-50 border border-blue-200 rounded-lg">
            <div className="flex items-center justify-center">
              <Loader className="w-6 h-6 text-blue-600 animate-spin mr-3" />
              <div>
                <p className="text-blue-800 font-medium">Processing your face swap...</p>
                <p className="text-blue-600 text-sm">This may take a few moments</p>
              </div>
            </div>
          </div>
        )}

        {/* Result Section */}
        {result && (
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-xl font-semibold text-gray-900 mb-4 text-center">
              Face Swap Result
            </h3>
            <div className="text-center">
              {result.result_url ? (
                <div className="space-y-4">
                  <img
                    src={result.result_url}
                    alt="Face swap result"
                    className="max-w-full h-auto rounded-lg shadow-md mx-auto"
                  />
                  <button
                    onClick={downloadResult}
                    className="inline-flex items-center px-6 py-3 bg-green-600 text-white font-semibold rounded-lg hover:bg-green-700 transition-colors"
                  >
                    <Download className="w-5 h-5 mr-2" />
                    Download Result
                  </button>
                </div>
              ) : (
                <div className="p-8 text-gray-600">
                  <CheckCircle className="w-12 h-12 text-green-500 mx-auto mb-4" />
                  <p className="text-lg font-medium">Face swap completed!</p>
                  <p className="mt-2">Processing ID: {result.processing_id}</p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Tips Section */}
        <div className="mt-12 bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Tips for Best Results</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-gray-600">
            <div className="space-y-2">
              <p>• Use high-quality images with good lighting</p>
              <p>• Ensure faces are clearly visible and not obscured</p>
              <p>• Front-facing photos work best</p>
            </div>
            <div className="space-y-2">
              <p>• Avoid extreme angles or side profiles</p>
              <p>• Images should be at least 512x512 pixels</p>
              <p>• Remove sunglasses or face coverings</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FaceSwap;
