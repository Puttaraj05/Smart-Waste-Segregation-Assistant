import os
import shutil
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img
import numpy as np

def augment_plastic_images():
    """
    Augment plastic images with proper error handling and separate output directory.
    """
    
    # Paths - using absolute paths for reliability
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(base_dir, '../../dataset/plastic/')
    output_dir = os.path.join(base_dir, '../../dataset/plastic_augmented/')
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Verify input directory exists
    if not os.path.exists(input_dir):
        print(f"Error: Input directory {input_dir} does not exist!")
        return
    
    # Data augmentation configuration
    augmenter = ImageDataGenerator(
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.15,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    
    # List all jpg files in the input directory
    try:
        image_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.jpg')]
        print(f"Found {len(image_files)} images to augment")
    except Exception as e:
        print(f"Error reading input directory: {e}")
        return
    
    if len(image_files) == 0:
        print("No images found to augment!")
        return
    
    augmented_count = 0
    
    for img_file in image_files:
        try:
            img_path = os.path.join(input_dir, img_file)
            img = load_img(img_path, target_size=(224, 224))
            x = img_to_array(img)
            x = np.expand_dims(x, axis=0)
            
            # Generate 5 augmented images per original
            i = 0
            for batch in augmenter.flow(x, batch_size=1, save_to_dir=output_dir, 
                                       save_prefix=f"aug_{img_file.split('.')[0]}", 
                                       save_format='jpg'):
                i += 1
                if i >= 5:
                    break
            
            augmented_count += 5
            
            if augmented_count % 50 == 0:
                print(f"Processed {augmented_count} augmented images...")
                
        except Exception as e:
            print(f"Error processing {img_file}: {e}")
            continue
    
    print(f"Augmentation complete! {augmented_count} augmented images saved to {output_dir}")

if __name__ == "__main__":
    augment_plastic_images() 