# 🫀 AI-Powered Cardiac ECG Detection & Explainable AI (XAI)

An end-to-end clinical decision support platform combining **Deep Learning (MobileNetV2)**, **Explainable AI (Grad-CAM)**, a **Flask REST API**, and a modern **React + Vite** frontend to detect cardiac anomalies from single-lead Electrocardiogram (ECG) tracings.

---

## 📌 Features

- **Automated ECG Analysis**: Binary classification distinguishing **Normal Sinus Rhythm** from **Myocardial Infarction (MI / Heart Attack)**.
- **Explainable AI (Grad-CAM Heatmaps)**: Utilizes `tf.GradientTape` and OpenCV (`cv2`) to highlight the exact ECG wave morphology (e.g., ST-elevation, T-wave inversion) that drove the model's decision.
- **Interactive Clinical Workflow**:
  - **Patient Intake**: Record patient identifiers, age, sex, and chief complaint.
  - **Diagnostic AI Core**: Upload ECG tracings with a projected medical millimeter grid (using CSS `mix-blend-mode`).
  - **Side-by-Side Review**: Compare original ECG tracings against the neural network heat focus map.
- **Multi-Model Support**: Pre-trained on the benchmark PhysioNet PTB-XL database (`cardiac_ptbxl_FINAL.keras`).

---

## 🏗️ Architecture

```
ECG Image Upload (React/Vite)
         │
         ▼  HTTP POST /analyze (FormData)
Flask Backend (port 5000)
         │
         ├─► Preprocessing: Resize 224x224 RGB, Normalize [0, 1]
         ├─► MobileNetV2 Inference: Sigmoid Output [0.0 - 1.0]
         └─► Grad-CAM Computation:
                 - tf.GradientTape watches MobileNetV2 feature maps
                 - Compute gradients with respect to target class loss
                 - Pool gradients & calculate class activation map
                 - OpenCV ColorMap JET overlay & Base64 encoding
         │
         ▼  JSON { diagnosis, confidence, is_normal, heatmap }
React Frontend Dashboard (Vite on port 5173)
```

---

## 📁 Repository Structure

```
.
├── Heart/
│   ├── api.py                 # Flask REST API backend (/analyze endpoint + Grad-CAM)
│   ├── app.py                 # Streamlit UI prototype
│   ├── train_model.py         # Model training script with MobileNetV2 & data augmentation
│   ├── fine_tune.py           # Transfer learning fine-tuning script
│   └── generate_images.py     # PTB-XL raw signal-to-image extraction pipeline
├── ecg-frontend/              # React 19 + Vite frontend
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Home.jsx       # Welcome landing page
│   │   │   ├── Details.jsx    # Patient intake form
│   │   │   └── Analyze.jsx    # ECG upload, analysis & heatmap visualizer
│   │   └── App.jsx            # React Router setup
│   ├── package.json
│   └── vite.config.js
├── sample_images/             # Lightweight test ECGs
│   ├── normal/                # Normal Sinus Rhythm samples
│   └── myocardial_infarction/ # Myocardial Infarction samples
├── cardiac_ptbxl_FINAL.keras  # Trained TensorFlow/Keras model (MobileNetV2)
├── requirements.txt           # Python backend dependencies
└── README.md                  # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+**
- **Node.js 18+ & npm**
- **Git**

---

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
```

---

### 2. Backend Setup (Python)

Create and activate a virtual environment:

```powershell
# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

Install backend dependencies:

```bash
pip install -r requirements.txt
```

Start the Flask API server:

```powershell
python Heart/api.py
```

*The API will start running at `http://127.0.0.1:5000`.*

---

### 3. Frontend Setup (React + Vite)

Open a **new terminal window**:

```powershell
cd ecg-frontend
npm install
npm run dev
```

*The frontend will launch at `http://localhost:5173`.*

---

## 🧪 Testing with Sample Images

1. Open `http://localhost:5173` in your browser.
2. Complete the patient intake details and proceed to the **Diagnostic AI Core**.
3. Upload any test image located in the [`sample_images/`](sample_images/) folder:
   - `sample_images/normal/normal_1.jpg`
   - `sample_images/myocardial_infarction/mi_1.jpg`
4. Click **Generate AI Report** to view diagnosis confidence and the Grad-CAM focus map.

---

## ⚠️ Medical Disclaimer

*This application is an educational and research prototype demonstrating Explainable AI for medical imaging. It is not approved for clinical diagnostic use. Real-world cardiac diagnosis requires a full 12-lead ECG and evaluation by a qualified medical professional.*