# Waste Classification AI Web Application

A modern web application that uses AI to classify waste materials and provide recycling guidance. Built with FastAPI backend and React frontend.

## Features

- 🖼️ **Image Upload**: Drag & drop or click to upload waste images
- 🤖 **AI Classification**: Powered by TensorFlow/Keras model
- ♻️ **Recycling Guidance**: Detailed information about waste types and disposal methods
- 📊 **Confidence Scores**: Visual representation of classification confidence
- 🎨 **Modern UI**: Beautiful, responsive design with Tailwind CSS
- 📱 **Mobile Friendly**: Works seamlessly on all devices

## Supported Waste Types

- **Biodegradable**: Natural materials that break down safely
- **Cardboard**: Recyclable paper-based material
- **Glass**: Recyclable glass containers
- **Metal**: Recyclable metal items (cans, foil)
- **Organic**: Food waste suitable for composting
- **Paper**: Recyclable paper products
- **Plastic**: Various plastic types (some recyclable)
- **Trash**: General waste for landfill

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **TensorFlow/Keras**: AI model for image classification
- **Pillow**: Image processing
- **NumPy**: Numerical computations

### Frontend
- **React**: Modern JavaScript framework
- **Vite**: Fast build tool and dev server
- **Tailwind CSS**: Utility-first CSS framework
- **Axios**: HTTP client for API calls
- **Lucide React**: Beautiful icons

## Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

## Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd waste
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
```

## Running the Application

### 1. Start the Backend Server

```bash
# From the backend directory
cd backend

# Activate virtual environment (if not already activated)
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows

# Start the FastAPI server
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at `http://localhost:8000`

### 2. Start the Frontend Development Server

```bash
# From the frontend directory
cd frontend

# Start the development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

### 3. Access the Application

Open your browser and navigate to `http://localhost:3000`

## Usage

1. **Upload Image**: Click "Choose File" or drag and drop an image of waste
2. **Analyze**: Click "Classify Waste" to process the image
3. **View Results**: See the classification, confidence score, and recycling guidance
4. **Learn**: Read the detailed description and tags for proper disposal

## API Endpoints

### POST /predict
Upload an image for waste classification.

**Request:**
- Content-Type: `multipart/form-data`
- Body: Image file

**Response:**
```json
{
  "prediction": {
    "label": "plastic",
    "confidence": 0.85,
    "tags": ["♻️ Recyclable", "🚯 Non-Biodegradable"],
    "description": "Plastics are non-biodegradable. Only some types are recyclable."
  },
  "all_probabilities": {
    "biodegradable": 0.02,
    "cardboard": 0.01,
    "glass": 0.03,
    "metal": 0.02,
    "organic": 0.01,
    "paper": 0.02,
    "plastic": 0.85,
    "trash": 0.04
  }
}
```

## Model Information

The application uses a pre-trained TensorFlow/Keras model that:
- Accepts 224x224 RGB images
- Outputs probabilities for 8 waste categories
- Uses a confidence threshold of 0.7 for reliable predictions
- Automatically downloads model files on first run

## Development

### Backend Development

```bash
cd backend
# Install development dependencies
pip install -r requirements.txt

# Run with auto-reload
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development

```bash
cd frontend
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

## Project Structure

```
waste/
├── backend/
│   ├── app.py              # FastAPI application
│   ├── requirements.txt    # Python dependencies
│   └── model/              # AI model files
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # Main React component
│   │   ├── main.jsx        # React entry point
│   │   └── index.css       # Global styles
│   ├── package.json        # Node.js dependencies
│   ├── vite.config.js      # Vite configuration
│   └── tailwind.config.js  # Tailwind CSS configuration
├── data/                   # Dataset files
├── models/                 # Model files
└── README.md              # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions, please open an issue on the GitHub repository.

---

**Note**: The AI model will automatically download required files on first run. Make sure you have a stable internet connection for the initial setup. 