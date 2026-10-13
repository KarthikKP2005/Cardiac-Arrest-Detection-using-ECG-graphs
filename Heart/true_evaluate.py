import tensorflow as tf
from tensorflow.keras.preprocessing import image_dataset_from_directory

data_dir = r"C:\Final\heart_ECG\ecg_data_new_version\ecg data new version"
img_size = (224, 224)
batch_size = 32

# Load the EXACT validation dataset we used during training
val_dataset = image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=img_size,
    batch_size=batch_size
)

# Normalize exactly as we did before
normalization_layer = tf.keras.layers.Rescaling(1./255)
val_dataset = val_dataset.map(lambda x, y: (normalization_layer(x), y))

print("\nLoading Final Boss Model...")
model = tf.keras.models.load_model(r"C:\Final\cardiac_cv_model_FINAL.keras")

print("\nGrading all 185 validation images...")
# evaluate() automatically loops through the entire dataset and calculates the exact score
loss, accuracy = model.evaluate(val_dataset)

print(f"\n--- TRUE MEDICAL ACCURACY ---")
print(f"Final Score: {accuracy * 100:.2f}%")