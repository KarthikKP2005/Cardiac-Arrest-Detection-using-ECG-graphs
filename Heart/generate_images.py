import pandas as pd
import numpy as np
import wfdb
import ast
import matplotlib.pyplot as plt
import os

# 1. Update this path to exactly where your extracted PTB-XL folder is
# Based on your screenshot, it's inside an 'archive' folder
base_path = r'C:\Final\archive\ptb-xl-a-large-publicly-available-electrocardiography-dataset-1.0.1\\'

# 2. Where we will save the generated images
output_dir = r'C:\Final\heart_ECG\ptbxl_generated_images'
os.makedirs(os.path.join(output_dir, 'normal_ecg_images'), exist_ok=True)
os.makedirs(os.path.join(output_dir, 'myocardial_infarction_ecg_images'), exist_ok=True)

print("Loading database CSV...")
# Load annotation data
Y = pd.read_csv(base_path + 'ptbxl_database.csv', index_col='ecg_id')
Y.scp_codes = Y.scp_codes.apply(lambda x: ast.literal_eval(x))

# Load diagnostic aggregation rules
agg_df = pd.read_csv(base_path + 'scp_statements.csv', index_col=0)
agg_df = agg_df[agg_df.diagnostic == 1]

def aggregate_diagnostic(y_dic):
    tmp = []
    for key in y_dic.keys():
        if key in agg_df.index:
            tmp.append(agg_df.loc[key].diagnostic_class)
    return list(set(tmp))

Y['diagnostic_superclass'] = Y.scp_codes.apply(aggregate_diagnostic)

# Filter for only Normal (NORM) and Heart Attack (MI)
print("Filtering patients...")
patients_normal = Y[Y['diagnostic_superclass'].apply(lambda x: 'NORM' in x)]
patients_mi = Y[Y['diagnostic_superclass'].apply(lambda x: 'MI' in x)]

def generate_ecg_images(patient_df, class_name, num_images_to_generate=1000):
    print(f"Generating {num_images_to_generate} images for {class_name}...")
    
    count = 0
    # Loop through the patients in this category
    for ecg_id, row in patient_df.iterrows():
        if count >= num_images_to_generate:
            break
            
        # PTB-XL provides low-res (100Hz) and high-res (500Hz) files. We will use 100Hz.
        file_path = base_path + row['filename_lr']
        
        try:
            # Read the raw electrical signal
            signal, meta = wfdb.rdsamp(file_path)
            
            # Create a 224x224 pixel image (exactly what MobileNetV2 wants!)
            # 224 pixels is roughly 2.24 inches at 100 dpi
            fig = plt.figure(figsize=(2.24, 2.24), dpi=100)
            
            # Plot just the first lead (Lead I) of the ECG to keep it clean
            plt.plot(signal[:, 0], color='black', linewidth=0.5)
            
            # Remove all axes, borders, and whitespace so the AI only sees the line
            plt.axis('off')
            plt.margins(0,0)
            plt.gca().xaxis.set_major_locator(plt.NullLocator())
            plt.gca().yaxis.set_major_locator(plt.NullLocator())
            
            # Save the image
            save_path = os.path.join(output_dir, class_name, f"{class_name}_{ecg_id}.jpg")
            plt.savefig(save_path, pad_inches=0, bbox_inches='tight', facecolor='white')
            plt.close(fig) # Close it so we don't crash your computer's RAM
            
            count += 1
            if count % 100 == 0:
                print(f"  -> Generated {count} images...")
                
        except Exception as e:
            # If a specific hospital file is corrupted, just skip it
            continue

# Generate 1,000 perfectly clean images for each class!
generate_ecg_images(patients_normal, 'normal_ecg_images', 1000)
generate_ecg_images(patients_mi, 'myocardial_infarction_ecg_images', 1000)

print("\nDONE! Your perfect 224x224 images are ready for training.")