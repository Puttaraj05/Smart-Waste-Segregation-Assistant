import os
import numpy as np
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import ResNet50V2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from sklearn.utils.class_weight import compute_class_weight
import pickle

# Try to import matplotlib for plotting
try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("matplotlib is not installed. Training plots will not be shown.")

def plot_training(history1, history2):
    if not MATPLOTLIB_AVAILABLE:
        print("matplotlib is not available. Cannot plot training history.")
        return
    plt.figure(figsize=(14, 5))
    # Accuracy
    plt.subplot(1, 2, 1)
    plt.plot(history1.history['accuracy'], label='Initial Train')
    plt.plot(history1.history['val_accuracy'], label='Initial Val')
    plt.plot(history2.history['accuracy'], label='Fine-tune Train')
    plt.plot(history2.history['val_accuracy'], label='Fine-tune Val')
    plt.title('Model Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.grid(True)
    # Loss
    plt.subplot(1, 2, 2)
    plt.plot(history1.history['loss'], label='Initial Train')
    plt.plot(history1.history['val_loss'], label='Initial Val')
    plt.plot(history2.history['loss'], label='Fine-tune Train')
    plt.plot(history2.history['val_loss'], label='Fine-tune Val')
    plt.title('Model Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def train_improved_waste_model():
    """
    Train an improved waste classification model with better architecture and data handling.
    """
    
    # Paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_dir = os.path.join(base_dir, '../../dataset')
    model_path = os.path.join(base_dir, 'waste_model_improved.keras')
    
    # Configuration
    img_size = (224, 224)
    batch_size = 16  # Reduced batch size for better training
    epochs = 30  # More epochs for better learning
    
    print("🔍 Checking dataset structure...")
    
    # Check available categories
    try:
        categories = [d for d in os.listdir(dataset_dir) 
                     if os.path.isdir(os.path.join(dataset_dir, d)) and not d.startswith('.')]
        print(f"Found categories: {categories}")
        
        # Check image counts per category
        for cat in categories:
            cat_path = os.path.join(dataset_dir, cat)
            img_count = len([f for f in os.listdir(cat_path) if f.lower().endswith('.jpg')])
            print(f"  {cat}: {img_count} images")
            
    except Exception as e:
        print(f"Error reading dataset: {e}")
        return
    
    # Data generators with proper augmentation
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        validation_split=0.2,
        rotation_range=30,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        vertical_flip=False,
        brightness_range=[0.8, 1.2],
        fill_mode='nearest'
    )
    
    # No augmentation for validation
    val_datagen = ImageDataGenerator(
        rescale=1./255,
        validation_split=0.2
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
        
        val_gen = val_datagen.flow_from_directory(
            dataset_dir,
            target_size=img_size,
            batch_size=batch_size,
            class_mode='categorical',
            subset='validation',
            shuffle=False
        )
        
        print(f"✅ Training samples: {train_gen.samples}")
        print(f"✅ Validation samples: {val_gen.samples}")
        print(f"✅ Classes: {list(train_gen.class_indices.keys())}")
        
    except Exception as e:
        print(f"Error creating data generators: {e}")
        return
    
    # Calculate class weights for imbalanced data
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
    
    # Create improved model using transfer learning
    try:
        print("🏗️ Building improved model...")
        
        # Use ResNet50V2 as base model
        base_model = ResNet50V2(
            weights='imagenet',
            include_top=False,
            input_shape=(*img_size, 3)
        )
        
        # Freeze base model layers
        base_model.trainable = False
        
        # Create new model
        model = keras.Sequential([
            base_model,
            GlobalAveragePooling2D(),
            Dense(512, activation='relu'),
            Dropout(0.5),
            Dense(256, activation='relu'),
            Dropout(0.3),
            Dense(len(classes), activation='softmax')
        ])
        
        # Compile model
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        print("Model architecture:")
        model.summary()
        
    except Exception as e:
        print(f"Error creating model: {e}")
        return
    
    # Callbacks for better training
    callbacks = [
        keras.callbacks.EarlyStopping(
            monitor='val_accuracy',
            patience=10,
            restore_best_weights=True
        ),
        keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-7
        ),
        keras.callbacks.ModelCheckpoint(
            filepath=os.path.join(base_dir, 'best_model.keras'),
            monitor='val_accuracy',
            save_best_only=True,
            verbose=1
        )
    ]
    
    # Train the model
    try:
        print("🚀 Starting training...")
        history = model.fit(
            train_gen,
            epochs=epochs,
            validation_data=val_gen,
            class_weight=class_weight_dict,
            callbacks=callbacks,
            verbose=1
        )
        
        print("✅ Training completed!")
        
        # Fine-tuning: Unfreeze some layers and train with lower learning rate
        print("🔧 Fine-tuning model...")
        base_model.trainable = True
        
        # Freeze early layers, unfreeze later layers
        for layer in base_model.layers[:-30]:
            layer.trainable = False
        
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.0001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        # Fine-tune for fewer epochs
        history_fine = model.fit(
            train_gen,
            epochs=15,
            validation_data=val_gen,
            class_weight=class_weight_dict,
            callbacks=callbacks,
            verbose=1
        )
        
        print("✅ Fine-tuning completed!")
        
        # 🔐 Save training history for later reuse
        with open(os.path.join(base_dir, 'training_history.pkl'), 'wb') as f:
            pickle.dump({'initial': history.history, 'fine_tune': history_fine.history}, f)
        print("📦 Training history saved to training_history.pkl")
        # 📊 Plot training and validation accuracy/loss
        plot_training(history, history_fine)
        
    except Exception as e:
        print(f"Error during training: {e}")
        return
    
    # Evaluate final model
    try:
        print("📊 Evaluating final model...")
        val_loss, val_accuracy = model.evaluate(val_gen, verbose=1)
        
        print(f"\n🎯 Final Model Performance:")
        print(f"   Validation Loss: {val_loss:.4f}")
        print(f"   Validation Accuracy: {val_accuracy:.4f} ({val_accuracy*100:.2f}%)")
        
        # Save the improved model
        model.save(model_path)
        print(f"💾 Model saved to {model_path}")
        
        # Also save in HDF5 format for compatibility
        h5_path = os.path.join(base_dir, 'waste_model_improved.h5')
        model.save(h5_path)
        print(f"💾 Model also saved to {h5_path}")
        
        # Print training history summary
        print(f"\n📈 Training Summary:")
        print(f"   Final Training Accuracy: {history.history['accuracy'][-1]:.4f}")
        print(f"   Best Validation Accuracy: {max(history.history['val_accuracy']):.4f}")
        
    except Exception as e:
        print(f"Error during evaluation: {e}")

if __name__ == "__main__":
    train_improved_waste_model() 