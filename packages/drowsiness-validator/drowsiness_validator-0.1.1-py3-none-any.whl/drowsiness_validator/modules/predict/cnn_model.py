import os
import numpy as np
import cv2
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt
import pkg_resources

# Constants
IMAGE_SIZE = (48, 48)  # Same dimensions used in your notebook
BATCH_SIZE = 32
EPOCHS = 10
# MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'drowsiness_cnn_model.h5') # Old path

def get_cnn_model_path():
    """Returns the path to the CNN model file within the package."""
    try:
        model_path = pkg_resources.resource_filename('drowsiness_validator', 'modules/predict/drowsiness_cnn_model.h5')
    except Exception as e:
        print(f"Error finding CNN model data file: {e}")
        model_path = os.path.join(os.path.dirname(__file__), 'drowsiness_cnn_model.h5')
        if not os.path.exists(model_path):
             raise FileNotFoundError("Could not find drowsiness_cnn_model.h5")
    return model_path

MODEL_PATH = get_cnn_model_path() # Set the model path using the function

def build_model():
    """Build and return a CNN model for drowsiness detection"""
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(IMAGE_SIZE[0], IMAGE_SIZE[1], 3)),
        MaxPooling2D((2, 2)),

        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),

        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),

        Flatten(),
        Dense(64, activation='relu'),
        Dropout(0.5),  # Add dropout for regularization
        Dense(1, activation='sigmoid')  # Binary classification: drowsy vs. natural
    ])

    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss='binary_crossentropy',
        metrics=['accuracy']
    )

    return model

def train_model(train_dir, test_dir):
    """Train the CNN model on the provided data directories"""
    # Data augmentation for training set
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        validation_split=0.2  # 20% of training data used for validation
    )

    # Only rescaling for test set
    test_datagen = ImageDataGenerator(rescale=1./255)

    # Set up the data generators
    train_gen = train_datagen.flow_from_directory(
        train_dir,
        target_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='binary',
        subset='training',
        shuffle=True
    )

    val_gen = train_datagen.flow_from_directory(
        train_dir,
        target_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='binary',
        subset='validation',
        shuffle=True
    )

    test_gen = test_datagen.flow_from_directory(
        test_dir,
        target_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='binary',
        shuffle=False
    )

    # Build the model
    model = build_model()
    print("Model architecture:")
    model.summary()

    # Train the model
    print("Training the model...")
    history = model.fit(
        train_gen,
        steps_per_epoch=train_gen.samples // BATCH_SIZE,
        epochs=EPOCHS,
        validation_data=val_gen,
        validation_steps=val_gen.samples // BATCH_SIZE
    )

    # Evaluate on test set
    print("Evaluating the model...")
    test_loss, test_accuracy = model.evaluate(test_gen)
    print(f"Test accuracy: {test_accuracy:.4f}")

    # Save the model
    model.save(MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

    # Plot training history
    plot_training_history(history)

    return model, history

def plot_training_history(history):
    """Plot the training and validation accuracy/loss"""
    # Plot training & validation accuracy
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('Model Accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Validation'], loc='upper left')

    # Plot training & validation loss
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('Model Loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Validation'], loc='upper left')

    plt.tight_layout()
    # Save plot in the same directory as the model
    plot_path = os.path.join(os.path.dirname(MODEL_PATH), 'training_history.png')
    try:
        plt.savefig(plot_path)
        print(f"Training history plot saved to {plot_path}")
    except Exception as e:
        print(f"Warning: Could not save training history plot: {e}")
    plt.close()

def predict_drowsiness_with_cnn(image_data=None, image_path=None, force_train=False, train_dir=None, test_dir=None):
    """Predict drowsiness using the trained CNN model from image data or path."""
    global MODEL_PATH # Ensure we use the globally defined path

    # Check if model exists, or train if forced
    if force_train:
        if not train_dir or not test_dir:
            raise ValueError("train_dir and test_dir must be provided when force_train=True")
        print("Forcing model training...")
        model, _ = train_model(train_dir, test_dir)
        MODEL_PATH = get_cnn_model_path() # Re-get path in case it was created
    elif not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model not found at {MODEL_PATH}. Train the model first or provide train/test dirs.")
    else:
        # Load the existing model
        try:
            model = load_model(MODEL_PATH)
        except Exception as e:
            raise RuntimeError(f"Failed to load model from {MODEL_PATH}: {e}")

    # Load and preprocess the image
    if image_data is not None:
        image = image_data # Use provided numpy array
    elif image_path is not None:
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not load image from path: {image_path}")
    else:
        raise ValueError("Either image_data or image_path must be provided.")

    # Preprocess the image
    try:
        # Resize image to match model's expected input
        image_resized = cv2.resize(image, IMAGE_SIZE)

        # Normalize pixel values
        image_normalized = image_resized / 255.0

        # Expand dimensions to match model's expected input shape (batch size of 1)
        image_expanded = np.expand_dims(image_normalized, axis=0)
    except Exception as e:
        raise ValueError(f"Error preprocessing image: {e}")

    # Make prediction
    try:
        prediction = model.predict(image_expanded)
        # Prediction is probability, threshold at 0.5
        is_drowsy = (prediction[0][0] > 0.5)
        confidence = prediction[0][0] if is_drowsy else 1 - prediction[0][0]
        return int(is_drowsy), float(confidence)
    except Exception as e:
        raise RuntimeError(f"Error during model prediction: {e}")

def train_model_if_needed(train_dir, test_dir, force_train=False):
    """Train the model if it doesn't exist or force_train is True"""
    # This function might be redundant now if predict handles force_train
    # Kept for potential separate training calls
    global MODEL_PATH
    if force_train or not os.path.exists(MODEL_PATH):
        print("Training required...")
        model, history = train_model(train_dir, test_dir)
        MODEL_PATH = get_cnn_model_path() # Update path after training
        return model, history
    else:
        print(f"Using existing model from {MODEL_PATH}")
        try:
            return load_model(MODEL_PATH), None
        except Exception as e:
            print(f"Warning: Failed to load existing model: {e}")
            return None, None

# Main execution for testing (requires train/test data outside package)
# if __name__ == "__main__":
#     # Paths to your data (adjust as needed)
#     base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#     train_dir_test = os.path.join(base_dir, "train")
#     test_dir_test = os.path.join(base_dir, "test")
#
#     # Train the model if needed (example)
#     # model, _ = train_model_if_needed(train_dir_test, test_dir_test, force_train=False)
#
#     # Test with a sample image
#     sample_image_path = os.path.join(base_dir, "images.jpeg") # Adjust path
#     if os.path.exists(sample_image_path):
#         try:
#             is_drowsy, confidence = predict_drowsiness_with_cnn(image_path=sample_image_path)
#             print(f"Prediction for {sample_image_path}: {'Drowsy' if is_drowsy == 1 else 'Active'} (confidence: {confidence:.2f})")
#         except Exception as e:
#             print(f"Error predicting {sample_image_path}: {e}")
#     else:
#         print(f"Sample image not found: {sample_image_path}")