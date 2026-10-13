import os

new_version_base = r"C:\Final\heart_ECG\ecg_data_new_version\ecg data new version"
deleted_count = 0

print("Scanning for duplicates...")
for root, dirs, files in os.walk(new_version_base):
    for file in files:
        # Find the exact duplicates we just made
        if file.startswith("stash_"):
            file_path = os.path.join(root, file)
            os.remove(file_path)
            deleted_count += 1

print(f"Cleanup complete! Removed {deleted_count} duplicate files.")