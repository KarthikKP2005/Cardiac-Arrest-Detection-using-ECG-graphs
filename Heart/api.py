from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import cv2 # NEW: For generating the heatmap
import base64
import os

app = Flask(__name__)
CORS(app)

model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "cardiac_ptbxl_FINAL.keras"))
if not os.path.exists(model_path):
    model_path = r"C:\Final\cardiac_ptbxl_FINAL.keras"

print(f"Loading AI Model from {model_path}...")
model = tf.keras.models.load_model(model_path)
print("Model loaded and ready!")

def generate_gradcam(img_array, model, prediction):
    # 1. We manually walk the image through the network to avoid graph-tracing bugs.
    # Convert image to a tensor
    x = tf.cast(img_array, tf.float32)
    
    # 2. Skip the data augmentation layer (layer 0) since we are not training!
    # Pass the image directly to MobileNetV2 (layer 1) to get the Feature Maps
    feature_maps = model.layers[1](x, training=False)
    
    # 3. Start the tape to watch these feature maps
    with tf.GradientTape() as tape:
        tape.watch(feature_maps)
        
        # 4. Pass the feature maps through your custom top layers manually
        y = model.layers[2](feature_maps)        # GlobalAveragePooling2D
        y = model.layers[3](y)                   # Dense (128)
        y = model.layers[4](y, training=False)   # Dropout
        preds = model.layers[5](y)               # Final Output Dense (1)
        
        # 5. Focus the gradient strictly on the diagnosis it made
        loss = preds[:, 0] if prediction >= 0.5 else 1.0 - preds[:, 0]

    # 6. Calculate the math: Gradients of the loss with respect to the feature maps
    grads = tape.gradient(loss, feature_maps)
    
    # 7. Pool the gradients and multiply by the feature maps to create the heat
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    feature_maps = feature_maps[0]
    heatmap = feature_maps @ tf.expand_dims(pooled_grads, -1)
    
    # 8. Clean up and normalize the heatmap so it looks good visually
    heatmap = tf.squeeze(heatmap)
    heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
    
    return heatmap.numpy()

@app.route('/analyze', methods=['POST'])
def analyze_ecg():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
        
    file = request.files['file']
    
    try:
        # Preprocess
        image = Image.open(io.BytesIO(file.read())).convert('RGB')
        img = image.resize((224, 224))
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, 0)

        # Make Prediction
        prediction = model.predict(img_array)[0][0]
        
        # --- GENERATE EXPLAINABLE AI HEATMAP ---
        heatmap = generate_gradcam(img_array, model, prediction)
        
        # Apply glowing jet colormap
        heatmap_cv = cv2.resize(heatmap, (224, 224))
        heatmap_cv = np.uint8(255 * heatmap_cv)
        heatmap_cv = cv2.applyColorMap(heatmap_cv, cv2.COLORMAP_JET)
        
        # Superimpose the heatmap over the original image
        original_img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        superimposed_img = cv2.addWeighted(original_img_cv, 0.5, heatmap_cv, 0.5, 0)
        
        # Convert to base64 so React can display it
        _, buffer = cv2.imencode('.jpg', superimposed_img)
        heatmap_base64 = base64.b64encode(buffer).decode('utf-8')
        # ----------------------------------------

        if prediction >= 0.5:
            diagnosis = "Normal Sinus Rhythm"
            confidence = float(prediction * 100)
            is_normal = True
        else:
            diagnosis = "Myocardial Infarction Detected"
            confidence = float((1 - prediction) * 100)
            is_normal = False
            
        return jsonify({
            "diagnosis": diagnosis,
            "confidence": round(confidence, 1),
            "is_normal": is_normal,
            "heatmap": heatmap_base64 # Sending the heatmap to the frontend!
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)