import os
import pickle

# Try to import matplotlib for plotting
try:
    import matplotlib.pyplot as plt
except ImportError:
    print("matplotlib is not installed. Please install it to see plots.")
    exit()

def plot_training(history1, history2):
    plt.figure(figsize=(14, 5))
    # Accuracy
    plt.subplot(1, 2, 1)
    plt.plot(history1['accuracy'], label='Initial Train')
    plt.plot(history1['val_accuracy'], label='Initial Val')
    plt.plot(history2['accuracy'], label='Fine-tune Train')
    plt.plot(history2['val_accuracy'], label='Fine-tune Val')
    plt.title('Model Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.grid(True)
    # Loss
    plt.subplot(1, 2, 2)
    plt.plot(history1['loss'], label='Initial Train')
    plt.plot(history1['val_loss'], label='Initial Val')
    plt.plot(history2['loss'], label='Fine-tune Train')
    plt.plot(history2['val_loss'], label='Fine-tune Val')
    plt.title('Model Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

base_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(base_dir, 'training_history.pkl'), 'rb') as f:
    histories = pickle.load(f)
plot_training(histories['initial'], histories['fine_tune'])
