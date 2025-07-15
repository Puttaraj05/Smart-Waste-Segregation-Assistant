import os
import numpy as np
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

def evaluate_waste_model():
    """
    Evaluate the trained waste classification model performance.
    """
    
    # Paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_dir = os.path.join(base_dir, '../../dataset')
    model_path = os.path.join(base_dir, 'waste_model.h5')
    
    # Load the trained model
    try:
        model = keras.models.load_model(model_path)
        print("✅ Model loaded successfully!")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return
    
    # Configuration
    img_size = (224, 224)
    batch_size = 32
    
    # Create test data generator (using validation split as test)
    test_datagen = ImageDataGenerator(rescale=1./255)
    
    try:
        test_gen = test_datagen.flow_from_directory(
            dataset_dir,
            target_size=img_size,
            batch_size=batch_size,
            class_mode='categorical',
            shuffle=False
        )
        
        print(f"✅ Test data loaded: {test_gen.samples} samples")
        print(f"✅ Categories: {list(test_gen.class_indices.keys())}")
        
    except Exception as e:
        print(f"❌ Error loading test data: {e}")
        return
    
    # Evaluate model
    try:
        print("\n🔍 Evaluating model performance...")
        test_loss, test_accuracy = model.evaluate(test_gen, verbose=1)
        
        print(f"\n📊 Model Performance:")
        print(f"   Test Loss: {test_loss:.4f}")
        print(f"   Test Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")
        
        # Predictions for detailed analysis
        predictions = model.predict(test_gen, verbose=1)
        predicted_classes = np.argmax(predictions, axis=1)
        true_classes = test_gen.classes
        
        # Classification report
        class_names = list(test_gen.class_indices.keys())
        print(f"\n📋 Classification Report:")
        print(classification_report(true_classes, predicted_classes, target_names=class_names))
        
        # Confusion matrix
        cm = confusion_matrix(true_classes, predicted_classes)
        
        # Plot confusion matrix
        plt.figure(figsize=(12, 10))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=class_names, yticklabels=class_names)
        plt.title('Confusion Matrix - Waste Classification Model')
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        plt.xticks(rotation=45)
        plt.yticks(rotation=0)
        plt.tight_layout()
        
        # Save the plot
        plot_path = os.path.join(base_dir, 'confusion_matrix.png')
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        print(f"📈 Confusion matrix saved to: {plot_path}")
        
        # Per-class accuracy
        print(f"\n📊 Per-Class Accuracy:")
        for i, class_name in enumerate(class_names):
            class_correct = cm[i, i]
            class_total = cm[i, :].sum()
            class_accuracy = class_correct / class_total if class_total > 0 else 0
            print(f"   {class_name}: {class_accuracy:.4f} ({class_correct}/{class_total})")
        
        # Overall assessment
        print(f"\n🎯 Model Assessment:")
        if test_accuracy >= 0.90:
            print("   🟢 EXCELLENT: Model trained very well (>90% accuracy)")
        elif test_accuracy >= 0.80:
            print("   🟡 GOOD: Model trained well (80-90% accuracy)")
        elif test_accuracy >= 0.70:
            print("   🟠 FAIR: Model trained adequately (70-80% accuracy)")
        else:
            print("   🔴 POOR: Model needs improvement (<70% accuracy)")
        
        # Check for overfitting indicators
        print(f"\n🔍 Overfitting Analysis:")
        if test_accuracy < 0.60:
            print("   ⚠️  Low accuracy might indicate underfitting or insufficient training")
        elif test_accuracy > 0.95:
            print("   ⚠️  Very high accuracy might indicate overfitting")
        else:
            print("   ✅ Accuracy seems reasonable")
            
    except Exception as e:
        print(f"❌ Error during evaluation: {e}")

if __name__ == "__main__":
    evaluate_waste_model() 