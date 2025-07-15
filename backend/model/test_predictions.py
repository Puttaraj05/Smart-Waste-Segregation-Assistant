import os
import numpy as np
from tensorflow import keras
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import random

def test_model_predictions():
    """
    Test the model predictions on random images from each category.
    """
    
    # Paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_dir = os.path.join(base_dir, '../../dataset')
    model_path = os.path.join(base_dir, 'waste_model_improved.h5')
    
    # Load the model
    try:
        model = keras.models.load_model(model_path)
        print("✅ Model loaded successfully!")
    except:
        try:
            model = keras.models.load_model(os.path.join(base_dir, 'waste_model.h5'))
            print("✅ Original model loaded successfully!")
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            return
    
    # Get categories
    categories = [d for d in os.listdir(dataset_dir) 
                 if os.path.isdir(os.path.join(dataset_dir, d)) and not d.startswith('.')]
    
    print(f"📁 Testing categories: {categories}")
    
    # Test predictions for each category
    for category in categories:
        print(f"\n🔍 Testing {category} category:")
        
        cat_path = os.path.join(dataset_dir, category)
        images = [f for f in os.listdir(cat_path) if f.lower().endswith('.jpg')]
        
        if len(images) == 0:
            print(f"   No images found in {category}")
            continue
        
        # Test 3 random images from this category
        for i in range(min(3, len(images))):
            img_file = random.choice(images)
            img_path = os.path.join(cat_path, img_file)
            
            try:
                # Load and preprocess image
                img = load_img(img_path, target_size=(224, 224))
                img_array = img_to_array(img)
                img_array = np.expand_dims(img_array, axis=0)
                img_array = img_array / 255.0
                
                # Make prediction
                predictions = model.predict(img_array, verbose=0)
                predicted_class = np.argmax(predictions[0])
                confidence = np.max(predictions[0])
                
                # Get class name
                predicted_category = categories[predicted_class]
                
                # Check if prediction is correct
                is_correct = predicted_category == category
                status = "✅ CORRECT" if is_correct else "❌ WRONG"
                
                print(f"   {img_file}: {predicted_category} ({confidence:.3f}) - {status}")
                
                # Show top 3 predictions
                top_3_indices = np.argsort(predictions[0])[-3:][::-1]
                print(f"     Top 3: ", end="")
                for idx in top_3_indices:
                    print(f"{categories[idx]}({predictions[0][idx]:.3f}) ", end="")
                print()
                
            except Exception as e:
                print(f"   Error processing {img_file}: {e}")

if __name__ == "__main__":
    test_model_predictions() 