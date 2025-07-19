import React, { useState } from 'react'
import { Upload, Camera, Trash2, Leaf, Recycle, AlertCircle, CheckCircle, Loader2 } from 'lucide-react'
import axios from 'axios'

function App() {
  const [selectedFile, setSelectedFile] = useState(null)
  const [preview, setPreview] = useState(null)
  const [prediction, setPrediction] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleFileSelect = (event) => {
    const file = event.target.files[0]
    if (file) {
      setSelectedFile(file)
      setPreview(URL.createObjectURL(file))
      setPrediction(null)
      setError(null)
    }
  }

  const handleDrop = (event) => {
    event.preventDefault()
    const file = event.dataTransfer.files[0]
    if (file && file.type.startsWith('image/')) {
      setSelectedFile(file)
      setPreview(URL.createObjectURL(file))
      setPrediction(null)
      setError(null)
    }
  }

  const handleDragOver = (event) => {
    event.preventDefault()
  }

  const predictWaste = async () => {
    if (!selectedFile) return

    setLoading(true)
    setError(null)

    const formData = new FormData()
    formData.append('file', selectedFile)

    try {
      const response = await axios.post('/predict', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      setPrediction(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to classify waste. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const getTagColor = (tag) => {
    if (tag.includes('♻️')) return 'bg-blue-100 text-blue-800'
    if (tag.includes('🌱')) return 'bg-green-100 text-green-800'
    if (tag.includes('🍃')) return 'bg-emerald-100 text-emerald-800'
    if (tag.includes('🍎')) return 'bg-orange-100 text-orange-800'
    if (tag.includes('🚯')) return 'bg-red-100 text-red-800'
    return 'bg-gray-100 text-gray-800'
  }

  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.8) return 'text-green-600'
    if (confidence >= 0.6) return 'text-yellow-600'
    return 'text-red-600'
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center mb-4">
            <Leaf className="w-8 h-8 text-green-600 mr-3" />
            <h1 className="text-4xl font-bold text-gray-900">Waste Classification AI</h1>
          </div>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Upload an image of waste to get instant AI-powered classification and recycling guidance
          </p>
        </div>

        <div className="max-w-4xl mx-auto">
          <div className="grid md:grid-cols-2 gap-8">
            {/* Upload Section */}
            <div className="card">
              <h2 className="text-2xl font-semibold mb-6 flex items-center">
                <Upload className="w-6 h-6 mr-2" />
                Upload Image
              </h2>

              {/* File Upload Area */}
              <div
                className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
                  selectedFile ? 'border-green-300 bg-green-50' : 'border-gray-300 hover:border-primary-400'
                }`}
                onDrop={handleDrop}
                onDragOver={handleDragOver}
              >
                {preview ? (
                  <div className="space-y-4">
                    <img
                      src={preview}
                      alt="Preview"
                      className="max-w-full h-48 object-cover rounded-lg mx-auto"
                    />
                    <div className="flex justify-center space-x-2">
                      <button
                        onClick={() => document.getElementById('file-input').click()}
                        className="btn-secondary"
                      >
                        Change Image
                      </button>
                      <button
                        onClick={() => {
                          setSelectedFile(null)
                          setPreview(null)
                          setPrediction(null)
                        }}
                        className="btn-secondary"
                      >
                        Remove
                      </button>
                    </div>
                  </div>
                ) : (
                  <div className="space-y-4">
                    <Camera className="w-12 h-12 text-gray-400 mx-auto" />
                    <div>
                      <p className="text-lg font-medium text-gray-700">
                        Drop your image here or click to browse
                      </p>
                      <p className="text-sm text-gray-500 mt-1">
                        Supports JPG, PNG, GIF up to 10MB
                      </p>
                    </div>
                    <button
                      onClick={() => document.getElementById('file-input').click()}
                      className="btn-primary"
                    >
                      Choose File
                    </button>
                  </div>
                )}
              </div>

              <input
                id="file-input"
                type="file"
                accept="image/*"
                onChange={handleFileSelect}
                className="hidden"
              />

              {selectedFile && (
                <button
                  onClick={predictWaste}
                  disabled={loading}
                  className="w-full btn-primary mt-6 flex items-center justify-center"
                >
                  {loading ? (
                    <>
                      <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                      Analyzing...
                    </>
                  ) : (
                    <>
                      <Trash2 className="w-5 h-5 mr-2" />
                      Classify Waste
                    </>
                  )}
                </button>
              )}
            </div>

            {/* Results Section */}
            <div className="card">
              <h2 className="text-2xl font-semibold mb-6 flex items-center">
                <Recycle className="w-6 h-6 mr-2" />
                Classification Results
              </h2>

              {error && (
                <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-4">
                  <div className="flex items-center">
                    <AlertCircle className="w-5 h-5 text-red-500 mr-2" />
                    <span className="text-red-700">{error}</span>
                  </div>
                </div>
              )}

              {loading && (
                <div className="text-center py-12">
                  <Loader2 className="w-12 h-12 text-primary-600 animate-spin mx-auto mb-4" />
                  <p className="text-gray-600">Analyzing your image...</p>
                </div>
              )}

              {prediction && !loading && (
                <div className="space-y-6 animate-fade-in">
                  {/* Main Prediction */}
                  <div className="bg-gradient-to-r from-primary-50 to-blue-50 rounded-lg p-6 border border-primary-200">
                    <div className="flex items-center justify-between mb-4">
                      <h3 className="text-xl font-semibold text-gray-900">
                        {prediction.prediction.label === 'uncertain' ? 'Uncertain Classification' : prediction.prediction.label}
                      </h3>
                      <div className="flex items-center">
                        {prediction.prediction.label === 'uncertain' ? (
                          <AlertCircle className="w-6 h-6 text-yellow-500" />
                        ) : (
                          <CheckCircle className="w-6 h-6 text-green-500" />
                        )}
                      </div>
                    </div>

                    <div className="mb-4">
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-sm font-medium text-gray-700">Confidence</span>
                        <span className={`text-sm font-semibold ${getConfidenceColor(prediction.prediction.confidence)}`}>
                          {(prediction.prediction.confidence * 100).toFixed(1)}%
                        </span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-primary-600 h-2 rounded-full transition-all duration-300"
                          style={{ width: `${prediction.prediction.confidence * 100}%` }}
                        ></div>
                      </div>
                    </div>

                    {prediction.prediction.tags && prediction.prediction.tags.length > 0 && (
                      <div className="mb-4">
                        <p className="text-sm font-medium text-gray-700 mb-2">Tags:</p>
                        <div className="flex flex-wrap gap-2">
                          {prediction.prediction.tags.map((tag, index) => (
                            <span
                              key={index}
                              className={`px-3 py-1 rounded-full text-xs font-medium ${getTagColor(tag)}`}
                            >
                              {tag}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}

                    {prediction.prediction.description && (
                      <div>
                        <p className="text-sm font-medium text-gray-700 mb-2">Description:</p>
                        <p className="text-sm text-gray-600">{prediction.prediction.description}</p>
                      </div>
                    )}
                  </div>

                  {/* All Probabilities */}
                  <div>
                    <h4 className="text-lg font-semibold mb-4">All Classifications</h4>
                    <div className="space-y-3">
                      {Object.entries(prediction.all_probabilities)
                        .sort(([, a], [, b]) => b - a)
                        .map(([className, probability]) => (
                          <div key={className} className="flex items-center justify-between">
                            <span className="text-sm font-medium text-gray-700 capitalize">
                              {className}
                            </span>
                            <div className="flex items-center space-x-2">
                              <div className="w-20 bg-gray-200 rounded-full h-2">
                                <div
                                  className="bg-primary-400 h-2 rounded-full"
                                  style={{ width: `${probability * 100}%` }}
                                ></div>
                              </div>
                              <span className="text-sm text-gray-600 w-12 text-right">
                                {(probability * 100).toFixed(1)}%
                              </span>
                            </div>
                          </div>
                        ))}
                    </div>
                  </div>
                </div>
              )}

              {!prediction && !loading && !error && (
                <div className="text-center py-12 text-gray-500">
                  <Trash2 className="w-12 h-12 mx-auto mb-4 opacity-50" />
                  <p>Upload an image to see classification results</p>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="text-center mt-12 pt-8 border-t border-gray-200">
          <p className="text-gray-600">
            Powered by AI • Helping you make better recycling decisions
          </p>
        </div>
      </div>
    </div>
  )
}

export default App 