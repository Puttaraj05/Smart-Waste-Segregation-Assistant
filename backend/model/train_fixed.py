import os
import numpy as np
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.utils.class_weight import compute_class_weight

def train_waste_classification_model():
    """
    Train waste classification model with proper error handling and modern Keras practices.
    """
    
    # Paths - using absolute paths for reliability
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_dir = os.path.join(base_dir, '../../dataset')
    model_path = os.path.join(base_dir, 'waste_model.keras')  # Using .keras format
    
    # Configuration
    img_size = (224, 224)
    batch_size = 32
    epochs = 15
    
    # Verify dataset directory exists
    if not os.path.exists(dataset_dir):
        print(f"Error: Dataset directory {dataset_dir} does not exist!")
        return
    
    # Check available categories
    try:
        categories = [d for d in os.listdir(dataset_dir) 
                     if os.path.isdir(os.path.join(dataset_dir, d)) and not d.startswith('.')]
        print(f"Found categories: {categories}")
    except Exception as e:
        print(f"Error reading dataset directory: {e}")
        return
    
    if len(categories) == 0:
        print("No categories found in dataset!")
        return
    
    # Data generators with augmentation
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        validation_split=0.2,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    
    try:
        train_gen = train_datagen.flow_from_directory(
            dataset_dir,
            target_size=img_size,
            batch_size=batch_size,
            class_mode='categorical',
            subset='training',
            shuffle=True
        )
        
        val_gen = train_datagen.flow_from_directory(
            dataset_dir,
            target_size=img_size,
            batch_size=batch_size,
            class_mode='categorical',
            subset='validation',
            shuffle=True
        )
        
        print(f"Training samples: {train_gen.samples}")
        print(f"Validation samples: {val_gen.samples}")
        
    except Exception as e:
        print(f"Error creating data generators: {e}")
        return
    
    # Calculate class weights
    try:
        classes = list(train_gen.class_indices.keys())
        class_counts = {cat: len(os.listdir(os.path.join(dataset_dir, cat))) for cat in classes}
        class_indices = {cls: idx for idx, cls in enumerate(classes)}
        
        y = []
        for cls in classes:
            y += [class_indices[cls]] * class_counts[cls]
        
        class_weights = compute_class_weight(class_weight='balanced', classes=np.unique(y), y=y)
        class_weight_dict = {i: w for i, w in enumerate(class_weights)}
        print('Class weights:', class_weight_dict)
        
    except Exception as e:
        print(f"Error calculating class weights: {e}")
        class_weight_dict = None
    
    # Modern CNN model with proper input layer
    try:
        model = keras.Sequential([
            keras.layers.Input(shape=(*img_size, 3)),  # Using shape instead of input_shape
            keras.layers.Conv2D(32, (3, 3), activation='relu'),
            keras.layers.MaxPooling2D(2, 2),
            keras.layers.Conv2D(64, (3, 3), activation='relu'),
            keras.layers.MaxPooling2D(2, 2),
            keras.layers.Conv2D(128, (3, 3), activation='relu'),
            keras.layers.MaxPooling2D(2, 2),
            keras.layers.Flatten(),
            keras.layers.Dense(128, activation='relu'),
            keras.layers.Dropout(0.5),  # Added dropout for regularization
            keras.layers.Dense(len(classes), activation='softmax')
        ])
        
        model.compile(
            optimizer='adam', 
            loss='categorical_crossentropy', 
            metrics=['accuracy']
        )
        
        print("Model architecture:")
        model.summary()
        
    except Exception as e:
        print(f"Error creating model: {e}")
        return
    
    # Train the model
    try:
        print("Starting training...")
        history = model.fit(
            train_gen,
            epochs=epochs,
            validation_data=val_gen,
            class_weight=class_weight_dict,
            verbose=1
        )
        
        print("Training completed successfully!")
        
    except Exception as e:
        print(f"Error during training: {e}")
        return
    
    # Save the model in modern format
    try:
        model.save(model_path)
        print(f'Model saved to {model_path}')
        
        # Also save in HDF5 format for compatibility if needed
        h5_path = os.path.join(base_dir, 'waste_model.h5')
        model.save(h5_path)
        print(f'Model also saved to {h5_path} for compatibility')
        
    except Exception as e:
        print(f"Error saving model: {e}")

if __name__ == "__main__":
    train_waste_classification_model() 