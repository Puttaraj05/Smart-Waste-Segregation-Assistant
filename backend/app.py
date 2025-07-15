from fastapi import FastAPI, UploadFile, File, Form, HTTPException
import os
from tensorflow import keras
from PIL import Image
import numpy as np
import io

app = FastAPI()

@app.on_event('startup')
def load_model():
    global model
    model_path = 'backend/model/waste_model_improved.h5'
    if not os.path.exists(model_path):
        raise RuntimeError(f"Model file not found at {model_path}")
    try:
        model = keras.models.load_model(model_path)
    except Exception as e:
        raise RuntimeError(f"Failed to load model: {e}")

class_names = ['biodegradable', 'cardboard', 'glass', 'metal', 'organic', 'paper', 'plastic', 'trash']

custom_class_map = {
    'cardboard': {
        "tags": ['♻️ Recyclable', '🌱 Biodegradable'],
        "description": "Cardboard is biodegradable and recyclable if clean and dry."
    },
    'glass': {
        "tags": ['♻️ Recyclable'],
        "description": "Glass is recyclable, but should be clean and unbroken."
    },
    'metal': {
        "tags": ['♻️ Recyclable'],
        "description": "Metal (like cans or foil) is recyclable when free from food or contaminants."
    },
    'paper': {
        "tags": ['♻️ Recyclable', '🌱 Biodegradable'],
        "description": "Paper is biodegradable and recyclable if not soiled."
    },
    'plastic': {
        "tags": ['♻️ Recyclable', '🚯 Non-Biodegradable'],
        "description": "Plastics are non-biodegradable. Only some types are recyclable."
    },
    'trash': {
        "tags": ['🚯 Non-Recyclable'],
        "description": "General waste (dirty, mixed, or non-recyclable items). Should go to landfill."
    },
    'biodegradable': {
        "tags": ['🌱 Biodegradable', '🍃 Eco-Friendly'],
        "description": "Biodegradable materials naturally break down and return to the earth safely."
    },
    'organic': {
        "tags": ['🍎 Organic Waste', '🌱 Biodegradable'],
        "description": "Organic waste includes food scraps and natural matter suitable for composting."
    }
}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert('RGB')
        image = image.resize((224, 224))
        img_array = np.array(image) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        preds = model.predict(img_array)
        probabilities = preds[0].tolist()
        pred_index = int(np.argmax(preds[0]))
        pred_class = class_names[pred_index]
        pred_confidence = float(probabilities[pred_index])
        class_info = custom_class_map.get(pred_class, {"tags": [], "description": ""})

        CONFIDENCE_THRESHOLD = 0.6  # Set your threshold here

        if pred_confidence < CONFIDENCE_THRESHOLD:
            return {
                "prediction": {
                    "label": "uncertain",
                    "confidence": round(pred_confidence, 4),
                    "tags": [],
                    "description": "The model is not confident in its prediction. The uploaded image may not match any known category."
                },
                "all_probabilities": {class_names[i]: round(float(probabilities[i]), 4) for i in range(len(class_names))}
            }

        return {
            "prediction": {
                "label": pred_class,
                "confidence": round(pred_confidence, 4),
                "tags": class_info["tags"],
                "description": class_info["description"]
            },
            "all_probabilities": {class_names[i]: round(float(probabilities[i]), 4) for i in range(len(class_names))}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 