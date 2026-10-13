import os
import shutil
import random

# The active folders your model trains on
new_version_base = r"C:\Final\heart_ECG\ecg_data_new_version\ecg data new version"

# The folders where your massive stash of old images is kept
# NOTE: If these folders are inside a 'Train' folder, update the paths accordingly!
# The folders where your massive stash of old images is kept
old_normal_dir = r"C:\Final\heart_ECG\ecg data old version\ecg data old version\test\Normal Person ECG Images (284x12=3408)"
old_abnormal_dir = r"C:\Final\heart_ECG\ecg data old version\ecg data old version\test\ECG Images of Patient that have abnormal heartbeat (233x12=2796)"
old_mi_dir = r"C:\Final\heart_ECG\ecg data old version\ecg data old version\test\ECG Images of Myocardial Infarction Patients (240x12=2880)"
old_post_mi_dir = r"C:\Final\heart_ECG\ecg data old version\ecg data old version\test\ECG Images of Patient that have History of MI (172x12=2064)"
# Map the old stash to the new active training folders
folder_mapping = {
    old_normal_dir: os.path.join(new_version_base, "normal_ecg_images"),
    old_abnormal_dir: os.path.join(new_version_base, "abnormal_heartbeat_ecg_images"),
    old_mi_dir: os.path.join(new_version_base, "myocardial_infarction_ecg_images"),
    old_post_mi_dir: os.path.join(new_version_base, "post_mi_history_ecg_images")
}

# The target size for EACH folder to prevent AI laziness (Class Imbalance)
TARGET_COUNT = 1000 

def balance_dataset():
    for source_dir, dest_dir in folder_mapping.items():
        print(f"\nProcessing: {os.path.basename(dest_dir)}")

        if not os.path.exists(source_dir):
            print(f"  -> ERROR: Could not find source folder:\n     {source_dir}")
            print("  -> Please check the path and try again.")
            continue

        # Count how many we already have in the active folder
        existing_images = len([f for f in os.listdir(dest_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
        print(f"  -> Current images in folder: {existing_images}")

        if existing_images >= TARGET_COUNT:
            print(f"  -> Already have enough images ({existing_images}). Skipping.")
            continue

        needed = TARGET_COUNT - existing_images
        print(f"  -> Need {needed} more images from the old stash...")

        # Find ALL images inside the old folder (os.walk digs into subfolders automatically)
        all_old_images = []
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    all_old_images.append(os.path.join(root, file))

        if not all_old_images:
            print("  -> No images found in source folder!")
            continue

        # Shuffle them to get a random, healthy sample
        random.seed(42)
        random.shuffle(all_old_images)

        # Copy the needed amount safely
        copied = 0
        for img_path in all_old_images:
            if copied >= needed:
                break

            # Add a prefix so we don't accidentally overwrite an existing file with the same name
            filename = os.path.basename(img_path)
            new_filename = f"stash_{copied}_{filename}"
            dest_path = os.path.join(dest_dir, new_filename)

            shutil.copy2(img_path, dest_path)
            copied += 1

        print(f"  -> Successfully merged {copied} new images!")

if __name__ == "__main__":
    print("--- STARTING DATASET MERGE ---")
    balance_dataset()
    print("\n--- DATASET BALANCING COMPLETE ---")