import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image

print("Loading model for batch test...")
model = tf.keras.models.load_model(r"C:\Final\cardiac_cv_model_FINAL.keras")

class_names = [
    'abnormal_heartbeat_ecg_images', 
    'myocardial_infarction_ecg_images', 
    'normal_ecg_images', 
    'post_mi_history_ecg_images'
]

folder_path = r"C:\Final\heart_ECG\ecg_data_new_version\ecg data new version\normal_ecg_images"
print(f"\nTesting up to 20 images in: {folder_path}\n")

correct_guesses = 0
total_tested = 0

for filename in os.listdir(folder_path)[:20]:
    if filename.lower().endswith((".jpg", ".png", ".jpeg")):
        img_path = os.path.join(folder_path, filename)
        
        # --- THE FIX: Perfect TensorFlow Preprocessing ---
        # 1. Load image at original massive size
        img = image.load_img(img_path) 
        img_array = image.img_to_array(img)
        
        # 2. Resize using TensorFlow's precise 'bilinear' method (matching training exactly)
        img_array = tf.image.resize(img_array, (224, 224)) 
        
        # 3. Normalize and format
        img_array = tf.expand_dims(img_array, 0) / 255.0
        # ------------------------------------------------
        
        predictions = model.predict(img_array, verbose=0)
        predicted_index = np.argmax(predictions[0])
        predicted_class = class_names[predicted_index]
        confidence = np.max(predictions[0]) * 100
        
        if predicted_class == 'normal_ecg_images':
            status = "✅ CORRECT"
            correct_guesses += 1
        else:
            status = f"❌ WRONG (Guessed: {predicted_class})"
            
        print(f"{filename}: {status} - {confidence:.1f}%")
        total_tested += 1

if total_tested > 0:
    accuracy = (correct_guesses / total_tested) * 100
    print(f"\n--- FINAL BATCH SCORE ---")
    print(f"Accuracy on this batch: {correct_guesses}/{total_tested} ({accuracy:.1f}%)")