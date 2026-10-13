import tensorflow as tf
from tensorflow.keras.preprocessing import image_dataset_from_directory
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import EarlyStopping # NEW: Import Early Stopping

data_dir = r"C:\Final\heart_ECG\ptbxl_generated_images"
img_size = (224, 224)
batch_size = 32

print("Loading datasets...")
train_dataset = image_dataset_from_directory(
    data_dir,
    validation_split=0.2, 
    subset="training",
    seed=123,             
    image_size=img_size,
    batch_size=batch_size
)

val_dataset = image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="validation",
    seed=123,             
    image_size=img_size,
    batch_size=batch_size
)

class_names = train_dataset.class_names
normalization_layer = tf.keras.layers.Rescaling(1./255)
train_dataset = train_dataset.map(lambda x, y: (normalization_layer(x), y))
val_dataset = val_dataset.map(lambda x, y: (normalization_layer(x), y))

# NEW: Create a medically-safe Data Augmentation pipeline
data_augmentation = tf.keras.Sequential([
    layers.RandomZoom(0.1),     # Slight zoom in/out (simulates camera distance)
    layers.RandomContrast(0.1), # Slight lighting changes
    # No flipping allowed for ECGs!
])

base_model = MobileNetV2(input_shape=(224, 224, 3), include_top=False, weights='imagenet')
base_model.trainable = False 

model = models.Sequential([
    data_augmentation,
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.2),
    layers.Dense(1, activation='sigmoid') # 1 node + sigmoid = Binary (Normal vs MI)
])

model.compile(optimizer='adam',
              loss='binary_crossentropy', # Changed for binary
              metrics=['accuracy'])

# NEW: Set up Early Stopping
# If validation loss doesn't improve for 5 epochs, stop training and keep the best weights.
early_stop = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

print("Starting training with Data Augmentation and Early Stopping...")
epochs = 50 # NEW: Increased from 10
history = model.fit(
    train_dataset,
    validation_data=val_dataset,
    epochs=epochs,
    callbacks=[early_stop] # NEW: Attach the safety net
)

# Save as a new file so we don't overwrite your V1
model.save(r"C:\Final\cardiac_ptbxl_v1.h5")
print("Model V3 saved successfully!")