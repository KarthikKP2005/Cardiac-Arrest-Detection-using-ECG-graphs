import sys
import json
import pickle
import pandas as pd
import numpy as np
import shap
import warnings

# Mute warnings so they don't corrupt the JSON response
warnings.filterwarnings('ignore')

# 1. Load the model
with open('cardiac_model.pkl', 'rb') as f:
    model = pickle.load(f)

def predict():
    try:
        # 2. Parse the frontend data
        input_json = sys.argv[1]
        patient_data = json.loads(input_json)
        df = pd.DataFrame([patient_data])
        
        # 3. Get the Risk Probability
        prob = model.predict_proba(df)[0][1] 
        
        # 4. THE ULTIMATE SHAP FIX (Black-Box Mode)
        # Instead of looking inside the buggy XGBoost trees, we create a custom function
        # that only returns the final probability. SHAP will test this function from the outside.
        predict_fn = lambda x: model.predict_proba(x)[:, 1]
        
        # We give SHAP a baseline of "Zeros" to compare the patient against
        background = pd.DataFrame(np.zeros((1, len(df.columns))), columns=df.columns)
        
        # Run the generic Explainer
        explainer = shap.Explainer(predict_fn, background)
        shap_values = explainer(df)
        
        # Extract the impact values
        vals = shap_values.values[0]
        
        # 5. Format the data for React
        explanation = []
        for i, feature in enumerate(df.columns):
            explanation.append({
                "name": feature.replace('_', ' ').title(),
                "Impact": round(float(vals[i]), 3)
            })
            
        # Sort to show the Top 5 most important factors
        explanation = sorted(explanation, key=lambda x: abs(x['Impact']), reverse=True)
        
        result = {
            "risk_score": round(float(prob) * 100, 2),
            "prediction": "High Risk" if prob > 0.5 else "Low Risk",
            "explanations": explanation[:5]
        }
        
        print(json.dumps(result))

    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    predict()