import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import os

# 1. Load your trained model
print("Loading model...")
# In predict.py, update this one line:
model = tf.keras.models.load_model(r"C:\Final\cardiac_cv_model_FINAL.keras")

# 2. These exact class names were extracted from your training logs
class_names = [
    'abnormal_heartbeat_ecg_images', 
    'myocardial_infarction_ecg_images', 
    'normal_ecg_images', 
    'post_mi_history_ecg_images'
]

def predict_ecg(image_path):
    if not os.path.exists(image_path):
        return f"Error: Could not find image at {image_path}"

    # Load and preprocess the image exactly like we did for training
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0) # Create a batch of 1
    img_array = img_array / 255.0 # Normalize pixels to 0-1

    # Make the prediction
    predictions = model.predict(img_array)
    
    # Extract the highest probability
    predicted_class_index = np.argmax(predictions[0])
    confidence = np.max(predictions[0]) * 100
    
    predicted_label = class_names[predicted_class_index]
    
    return f"\n--- RESULTS ---\nDiagnosis: {predicted_label}\nConfidence: {confidence:.2f}%\n---------------"

# 3. Test it with a real image!
# IMPORTANT: You need to replace "filename.jpg" with the actual name of an image in that folder
test_image_path = r"C:\Final\heart_ECG\ecg_data_new_version\ecg data new version\normal_ecg_images\Normal(1).jpg" 

print(predict_ecg(test_image_path))