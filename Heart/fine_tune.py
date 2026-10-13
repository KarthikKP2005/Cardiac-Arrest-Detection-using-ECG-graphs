import tensorflow as tf
from tensorflow.keras.preprocessing import image_dataset_from_directory
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau

# 1. Pointing to your clean, generated dataset
data_dir = r"C:\Final\heart_ECG\ptbxl_generated_images"
img_size = (224, 224)
batch_size = 32

print("Loading datasets...")
train_dataset = image_dataset_from_directory(
    data_dir, validation_split=0.2, subset="training", seed=123,
    image_size=img_size, batch_size=batch_size
)
val_dataset = image_dataset_from_directory(
    data_dir, validation_split=0.2, subset="validation", seed=123,
    image_size=img_size, batch_size=batch_size
)

normalization_layer = tf.keras.layers.Rescaling(1./255)
train_dataset = train_dataset.map(lambda x, y: (normalization_layer(x), y))
val_dataset = val_dataset.map(lambda x, y: (normalization_layer(x), y))

print("Loading PTB-XL Model for Deep Fine-Tuning...")
model = tf.keras.models.load_model(r"C:\Final\cardiac_ptbxl_v1.h5")

base_model = model.layers[1] 
base_model.trainable = True

# Unfreeze the top layers
fine_tune_at = 50
for layer in base_model.layers[:fine_tune_at]:
    layer.trainable = False

# CRITICAL: Lock Batch Normalization so we don't destroy existing knowledge
for layer in base_model.layers:
    if isinstance(layer, tf.keras.layers.BatchNormalization):
        layer.trainable = False

# CRITICAL: Binary Crossentropy for 2 classes!
model.compile(loss='binary_crossentropy',
              optimizer=tf.keras.optimizers.Adam(learning_rate=0.00001), 
              metrics=['accuracy'])

# The "Pro-Level" Callbacks
lr_scheduler = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=2, min_lr=1e-7, verbose=1)
early_stop = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True, verbose=1)

print("Starting Deep Fine-Tuning...")
epochs = 15 
history_fine = model.fit(
    train_dataset,
    validation_data=val_dataset,
    epochs=epochs,
    callbacks=[early_stop, lr_scheduler]
)

# Save into the modern, bug-free format
model.save(r"C:\Final\cardiac_ptbxl_FINAL.keras")
print("New FINAL PTB-XL Model saved successfully!")