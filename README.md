# Smart Waste Segregation Assistant

This project is an AI-powered web application that helps users sort waste at home using image classification (recyclable, organic, hazardous, etc.).

## Project Structure

```
waste/
│
├── backend/
│   ├── model/
│   │   ├── train.py           # Script to train and save your Keras model (.h5)
│   │   └── waste_model.h5     # Saved Keras model (after training)
│   ├── app.py                 # FastAPI app to serve predictions
│   └── requirements.txt       # Backend dependencies
│
├── frontend/
│   ├── public/
│   │   └── index.html         # Main HTML file
│   ├── src/
│   │   ├── App.js             # Main React component
│   │   └── api.js             # JS to call backend API
│   └── package.json           # Frontend dependencies
│
├── dataset/                   # Place your dataset here
│   └── (your_dataset_files)
│
└── README.md                  # Project overview and setup instructions
```

## Setup Instructions

### 1. Backend (FastAPI)
- Go to the `backend/` directory.
- Install dependencies: `pip3 install -r requirements.txt`
- Train your model: `python3 model/train.py`
- Start the API server: `uvicorn app:app --reload`

### 2. Frontend (React)
- Go to the `frontend/` directory.
- Install dependencies: `npm install`
- Start the development server: `npm start`

### 3. Dataset
- Place your dataset files in the `dataset/` directory.

---

## How it Works
1. User uploads an image via the web interface.
2. The image is sent to the backend API.
3. The backend uses the trained model to predict the waste type.
4. The result is displayed to the user. 

---

## Backend API Usage

### POST `/predict`
- **Description:** Upload an image to classify the type of waste.
- **Request:**
  - `file`: Image file (form-data)
- **Response:**
  - `prediction.label`: Predicted class label (e.g., 'plastic', 'organic', etc.)
  - `prediction.confidence`: Confidence score (0 to 1)
  - `prediction.tags`: List of tags for the class
  - `prediction.description`: Description of the class
  - `all_probabilities`: Dictionary of all class probabilities

#### Example Response
```
{
  "prediction": {
    "label": "plastic",
    "confidence": 0.87,
    "tags": ["♻️ Recyclable", "🚯 Non-Biodegradable"],
    "description": "Plastics are non-biodegradable. Only some types are recyclable."
  },
  "all_probabilities": {
    "biodegradable": 0.01,
    "cardboard": 0.02,
    "glass": 0.01,
    "metal": 0.01,
    "organic": 0.01,
    "paper": 0.01,
    "plastic": 0.87,
    "trash": 0.06
  }
}
```

### Confidence Threshold
- If the model's confidence is below **0.6**, the API will return:
  - `label`: `"uncertain"`
  - `description`: "The model is not confident in its prediction. The uploaded image may not match any known category."

### Class Order Requirement
- The `class_names` in the backend **must match the alphabetical order of your dataset folders**. If you change your dataset, update the class order in `app.py` accordingly.

---

## Troubleshooting
- If predictions are incorrect, check that:
  - The class order in `app.py` matches your training data.
  - The model file is up to date and matches your dataset.
  - The image preprocessing (size, normalization) matches your training pipeline.
- For images outside the training categories, the model will still return a prediction, but it may be labeled as `"uncertain"` if confidence is low.

--- 

## 📦 Model & Dataset Downloads

To use the model and dataset, download them from the links below or let the script auto-download:

- 🧠 `model1.keras`: [Download from Google Drive](https://drive.google.com/file/d/1EEVdZIccpaoae4YXqufto06sVf7kgdid/view?usp=sharing)
- 🧠 `model2.h5`: [Download from Google Drive](https://drive.google.com/file/d/13adspLBtZpSoABp4VkWjBITwWvelft6x/view?usp=sharing)
- 📁 `dataset.zip`: [Download from Google Drive](https://drive.google.com/file/d/1Ifv5aCXVo0TDHK8K8XsrF77dk7rr83p4/view?usp=sharing) 