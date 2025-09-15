import React, { useState, useRef, useEffect } from 'react';
import { Camera, Upload, Download, Palette, AlertCircle, CheckCircle, Loader, Play, Pause } from 'lucide-react';
import { applyARMask } from '../services/api';

const ARMask = () => {
  const [selectedMask, setSelectedMask] = useState(null);
  const [uploadedImage, setUploadedImage] = useState(null);
  const [result, setResult] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState(null);
  const [useCamera, setUseCamera] = useState(false);
  const [stream, setStream] = useState(null);
  
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const fileInputRef = useRef(null);

  const availableMasks = [
    {
      id: 'dog',
      name: 'Dog Filter',
      preview: '/masks/dog-preview.jpg',
      description: 'Cute dog ears and nose'
    },
    {
      id: 'cat',
      name: 'Cat Filter',
      preview: '/masks/cat-preview.jpg',
      description: 'Adorable cat ears and whiskers'
    },
    {
      id: 'bunny',
      name: 'Bunny Filter',
      preview: '/masks/bunny-preview.jpg',
      description: 'Fluffy bunny ears'
    },
    {
      id: 'crown',
      name: 'Royal Crown',
      preview: '/masks/crown-preview.jpg',
      description: 'Elegant golden crown'
    },
    {
      id: 'glasses',
      name: 'Cool Glasses',
      preview: '/masks/glasses-preview.jpg',
      description: 'Stylish sunglasses'
    },
    {
      id: 'flower',
      name: 'Flower Crown',
      preview: '/masks/flower-preview.jpg',
      description: 'Beautiful flower headband'
    }
  ];

  useEffect(() => {
    return () => {
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
      }
    };
  }, [stream]);

  const startCamera = async () => {
    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({ 
        video: { width: 640, height: 480 } 
      });
      setStream(mediaStream);
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
      }
      setUseCamera(true);
      setError(null);
    } catch (err) {
      setError('Unable to access camera. Please check permissions.');
    }
  };

  const stopCamera = () => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      setStream(null);
    }
    setUseCamera(false);
  };

  const capturePhoto = () => {
    if (videoRef.current && canvasRef.current) {
      const canvas = canvasRef.current;
      const video = videoRef.current;
      const context = canvas.getContext('2d');
      
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      context.drawImage(video, 0, 0);
      
      canvas.toBlob((blob) => {
        const file = new File([blob], 'camera-capture.jpg', { type: 'image/jpeg' });
        setUploadedImage({ 
          file, 
          preview: canvas.toDataURL() 
        });
        stopCamera();
      });
    }
  };

  const handleFileUpload = (file) => {
    if (!file.type.startsWith('image/')) {
      setError('Please upload a valid image file');
      return;
    }

    const reader = new FileReader();
    reader.onload = (e) => {
      setUploadedImage({ file, preview: e.target.result });
      setError(null);
      setResult(null);
    };
    reader.readAsDataURL(file);
  };

  const handleInputChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      handleFileUpload(file);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file) {
      handleFileUpload(file);
    }
  };

  const handleSubmit = async () => {
    if (!selectedMask || !uploadedImage) {
      setError('Please select a mask and upload an image');
      return;
    }

    setIsProcessing(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('image', uploadedImage.file);
      formData.append('mask_type', selectedMask.id);

      const response = await applyARMask(formData);
      
      if (response.success) {
        setResult(response);
      } else {
        setError(response.error || 'AR mask application failed');
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
      link.download = 'ar-mask-result.jpg';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  };

  const reset = () => {
    setSelectedMask(null);
    setUploadedImage(null);
    setResult(null);
    setError(null);
    setIsProcessing(false);
    stopCamera();
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            AR Mask Studio
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Apply stunning AR masks and filters to your photos with advanced face tracking technology
          </p>
        </div>

        {/* Error Alert */}
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-center">
            <AlertCircle className="w-5 h-5 text-red-500 mr-3 flex-shrink-0" />
            <span className="text-red-700">{error}</span>
          </div>
        )}

        {/* Mask Selection */}
        <div className="mb-8">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Choose Your Mask</h3>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
            {availableMasks.map((mask) => (
              <div
                key={mask.id}
                onClick={() => setSelectedMask(mask)}
                className={`cursor-pointer rounded-lg border-2 transition-all ${
                  selectedMask?.id === mask.id
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <div className="p-4 text-center">
                  <div className="w-16 h-16 mx-auto mb-2 bg-gradient-to-br from-purple-400 to-pink-400 rounded-full flex items-center justify-center">
                    <Palette className="w-8 h-8 text-white" />
                  </div>
                  <h4 className="font-medium text-gray-900 text-sm">{mask.name}</h4>
                  <p className="text-xs text-gray-500 mt-1">{mask.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Image Upload Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Upload Options */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Upload Your Photo</h3>
            
            {!useCamera ? (
              <div
                className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-gray-400 transition-colors"
                onDrop={handleDrop}
                onDragOver={(e) => e.preventDefault()}
              >
                {uploadedImage ? (
                  <div className="space-y-4">
                    <img
                      src={uploadedImage.preview}
                      alt="Uploaded preview"
                      className="w-full h-48 object-cover rounded-lg shadow-md"
                    />
                    <div className="flex items-center justify-center text-green-600">
                      <CheckCircle className="w-5 h-5 mr-2" />
                      <span className="font-medium">Image uploaded</span>
                    </div>
                    <button
                      onClick={() => fileInputRef.current?.click()}
                      className="text-blue-600 hover:text-blue-700 font-medium"
                    >
                      Change image
                    </button>
                  </div>
                ) : (
                  <div className="space-y-4">
                    <Upload className="w-12 h-12 text-gray-400 mx-auto" />
                    <div>
                      <p className="text-lg font-medium text-gray-700">Upload Image</p>
                      <p className="text-gray-500 mt-1">Choose a photo to apply the AR mask</p>
                    </div>
                    <div className="flex flex-col sm:flex-row gap-3 justify-center">
                      <button
                        onClick={() => fileInputRef.current?.click()}
                        className="inline-flex items-center px-4 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors"
                      >
                        <Upload className="w-4 h-4 mr-2" />
                        Choose File
                      </button>
                      <button
                        onClick={startCamera}
                        className="inline-flex items-center px-4 py-2 border border-gray-300 text-gray-700 font-medium rounded-lg hover:bg-gray-50 transition-colors"
                      >
                        <Camera className="w-4 h-4 mr-2" />
                        Use Camera
                      </button>
                    </div>
                    <p className="text-sm text-gray-400">or drag and drop an image here</p>
                  </div>
                )}
              </div>
            ) : (
              <div className="space-y-4">
                <div className="bg-black rounded-lg overflow-hidden">
                  <video
                    ref={videoRef}
                    autoPlay
                    playsInline
                    className="w-full h-auto"
                  />
                </div>
                <div className="flex gap-3 justify-center">
                  <button
                    onClick={capturePhoto}
                    className="inline-flex items-center px-4 py-2 bg-green-600 text-white font-medium rounded-lg hover:bg-green-700 transition-colors"
                  >
                    <Camera className="w-4 h-4 mr-2" />
                    Capture Photo
                  </button>
                  <button
                    onClick={stopCamera}
                    className="inline-flex items-center px-4 py-2 border border-gray-300 text-gray-700 font-medium rounded-lg hover:bg-gray-50 transition-colors"
                  >
                    <Pause className="w-4 h-4 mr-2" />
                    Stop Camera
                  </button>
                </div>
              </div>
            )}

            <input
              ref={fileInputRef}
              type="file"
              className="hidden"
              accept="image/*"
              onChange={handleInputChange}
            />
          </div>

          {/* Preview Section */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Preview</h3>
            <div className="bg-white rounded-lg shadow-md p-6 h-full flex items-center justify-center min-h-64">
              {selectedMask && uploadedImage ? (
                <div className="text-center space-y-4">
                  <div className="relative">
                    <img
                      src={uploadedImage.preview}
                      alt="Preview"
                      className="w-48 h-48 object-cover rounded-lg shadow-md mx-auto"
                    />
                    <div className="absolute inset-0 bg-gradient-to-r from-purple-500/20 to-pink-500/20 rounded-lg flex items-center justify-center">
                      <div className="bg-white/90 rounded-full p-3">
                        <Palette className="w-8 h-8 text-purple-600" />
                      </div>
                    </div>
                  </div>
                  <p className="text-sm text-gray-600">
                    Ready to apply <strong>{selectedMask.name}</strong>
                  </p>
                </div>
              ) : (
                <div className="text-center text-gray-400">
                  <Palette className="w-16 h-16 mx-auto mb-4" />
                  <p>Select a mask and upload an image to see preview</p>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center mb-8">
          <button
            onClick={handleSubmit}
            disabled={!selectedMask || !uploadedImage || isProcessing}
            className="inline-flex items-center px-8 py-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white font-semibold rounded-lg hover:from-purple-700 hover:to-pink-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
          >
            {isProcessing ? (
              <Loader className="w-5 h-5 mr-2 animate-spin" />
            ) : (
              <Palette className="w-5 h-5 mr-2" />
            )}
            {isProcessing ? 'Applying Mask...' : 'Apply AR Mask'}
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
          <div className="mb-8 p-6 bg-purple-50 border border-purple-200 rounded-lg">
            <div className="flex items-center justify-center">
              <Loader className="w-6 h-6 text-purple-600 animate-spin mr-3" />
              <div>
                <p className="text-purple-800 font-medium">Applying AR mask...</p>
                <p className="text-purple-600 text-sm">Processing with AI face tracking</p>
              </div>
            </div>
          </div>
        )}

        {/* Result Section */}
        {result && (
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-xl font-semibold text-gray-900 mb-4 text-center">
              AR Mask Result
            </h3>
            <div className="text-center">
              {result.result_url ? (
                <div className="space-y-4">
                  <img
                    src={result.result_url}
                    alt="AR mask result"
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
                  <p className="text-lg font-medium">AR mask applied successfully!</p>
                  <p className="mt-2">Processing ID: {result.processing_id}</p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Hidden canvas for photo capture */}
        <canvas ref={canvasRef} className="hidden" />

        {/* Tips Section */}
        <div className="mt-12 bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Tips for Best Results</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-gray-600">
            <div className="space-y-2">
              <p>• Use well-lit photos with clear face visibility</p>
              <p>• Face the camera directly for optimal tracking</p>
              <p>• Ensure the face takes up a good portion of the image</p>
            </div>
            <div className="space-y-2">
              <p>• Avoid extreme angles or tilted heads</p>
              <p>• Remove existing glasses or face coverings</p>
              <p>• Higher resolution images yield better results</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ARMask;
