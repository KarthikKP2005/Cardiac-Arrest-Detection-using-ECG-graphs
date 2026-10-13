import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

import os

# 1. Setup the Webpage
st.set_page_config(page_title="AI ECG Analyzer", layout="centered")
st.title("🫀 AI Cardiac ECG Analyzer")
st.write("Upload an ECG image to let the AI detect if it is Normal or shows signs of Myocardial Infarction.")

# 2. Load the Model (st.cache_resource keeps it loaded in memory so it's fast)
@st.cache_resource
def load_model():
    model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "cardiac_ptbxl_FINAL.keras"))
    if not os.path.exists(model_path):
        model_path = r"C:\Final\cardiac_ptbxl_FINAL.keras"
    return tf.keras.models.load_model(model_path)

try:
    model = load_model()
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# 3. Create the File Uploader
uploaded_file = st.file_uploader("Choose a 224x224 ECG image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # 4. Display the Image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded ECG', use_container_width=True)

    st.write("🧠 Analyzing...")

    # 5. Preprocess the image exactly like our training script
    img = image.resize((224, 224))
    img_array = np.array(img)
    
    # Ensure the image has 3 color channels (RGB)
    if len(img_array.shape) == 2: # If it's grayscale
        img_array = np.stack((img_array,)*3, axis=-1)
    elif img_array.shape[2] == 4: # If it has transparency (RGBA)
        img_array = img_array[..., :3]
        
    img_array = np.expand_dims(img_array, 0) / 255.0

    # 6. Make the Prediction
    prediction = model.predict(img_array)[0][0]
    
    # Because 'myocardial_infarction_ecg_images' comes first alphabetically, 
    # it is Class 0. 'normal_ecg_images' is Class 1.
    if prediction >= 0.5:
        diagnosis = "Normal ECG"
        confidence = prediction * 100
        st.success(f"**Diagnosis:** ✅ {diagnosis} (Confidence: {confidence:.1f}%)")
    else:
        diagnosis = "Myocardial Infarction"
        confidence = (1 - prediction) * 100
        st.error(f"**Diagnosis:** ⚠️ {diagnosis} (Confidence: {confidence:.1f}%)")