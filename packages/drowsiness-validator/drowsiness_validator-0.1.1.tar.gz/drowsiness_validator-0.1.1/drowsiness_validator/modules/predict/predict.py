import pandas as pd
import os
import pkg_resources
# from sklearn.tree import DecisionTreeClassifier # Comment out Decision Tree
from sklearn.ensemble import RandomForestClassifier # Import RandomForestClassifier
from sklearn.model_selection import train_test_split # Import train_test_split
from sklearn.metrics import accuracy_score # Import accuracy_score for evaluation
# Use relative import for cnn_model
from .cnn_model import predict_drowsiness_with_cnn, train_model_if_needed, get_cnn_model_path

# Constants
USE_CNN = True  # Set to True to use CNN model, False to use Random Forest

# Function to get the path to the data file within the package
def get_dataset_path():
    try:
        # Adjust the resource path based on the structure defined in setup.py
        dataset_path = pkg_resources.resource_filename('drowsiness_validator', 'modules/predict/drowsiness_dataset.csv')
    except Exception as e:
        print(f"Error finding dataset data file: {e}")
        # Fallback or error handling if the resource isn't found
        dataset_path = os.path.join(os.path.dirname(__file__), 'drowsiness_dataset.csv')
        if not os.path.exists(dataset_path):
             # Decide if this is critical. Maybe RF model is optional?
             print("Warning: Could not find drowsiness_dataset.csv for Random Forest model.")
             return None
    return dataset_path

# Paths for CNN model (now handled within cnn_model.py)
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# TRAIN_DIR = os.path.join(BASE_DIR, "train") # Assuming train/test dirs are outside the package for training
# TEST_DIR = os.path.join(BASE_DIR, "test")

# --- Random Forest Model Initialization ---
model = None # Initialize model to None
dataset_path = get_dataset_path()
if not USE_CNN and dataset_path:
    try:
        dataframe = pd.read_csv(dataset_path)
        X = dataframe.drop(columns=['drowsy'])
        y = dataframe['drowsy']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = RandomForestClassifier(random_state=42, n_estimators=100)
        model.fit(X_train, y_train)
        y_pred_test = model.predict(X_test)
        test_accuracy = accuracy_score(y_test, y_pred_test)
        print(f"Random Forest Model Test Accuracy: {test_accuracy:.4f}")
    except Exception as e:
        print(f"Error initializing Random Forest model: {e}")
elif not USE_CNN and not dataset_path:
    print("Cannot initialize Random Forest model: Dataset not found.")

# --- CNN Model Handling ---
cnn_model_loaded = False
if USE_CNN:
    try:
        # Check if the model file exists using the function from cnn_model
        if os.path.exists(get_cnn_model_path()):
             # We don't need to explicitly load it here, predict_drowsiness_with_cnn handles loading.
             print("CNN model file found.")
             cnn_model_loaded = True
        else:
             # Training logic might need external data paths if triggered here
             print(f"CNN model file not found at {get_cnn_model_path()}. Training may be required externally or via force_train.")
             # Optionally, try to train if train/test data paths are known/provided
             # train_model_if_needed(TRAIN_DIR, TEST_DIR, force_train=False) # Requires TRAIN_DIR/TEST_DIR
    except Exception as e:
        print(f"Warning: Error checking/loading CNN model: {e}")
        # Fallback logic if needed
        if not USE_CNN and model is None and dataset_path: # Try RF again if CNN fails and RF wasn't primary
             print("Falling back to Random Forest model due to CNN error.")
             USE_CNN = False
             try:
                 dataframe = pd.read_csv(dataset_path)
                 X = dataframe.drop(columns=['drowsy'])
                 y = dataframe['drowsy']
                 X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                 model = RandomForestClassifier(random_state=42, n_estimators=100)
                 model.fit(X_train, y_train)
             except Exception as rf_e:
                 print(f"Error initializing fallback Random Forest model: {rf_e}")

# Updated predict_drowsiness function (renamed to avoid conflict with api.py)
def predict_drowsiness_internal(image_data=None, force_train=False, aspect_ratios=None):
    """
    Internal prediction function called by the main API.
    Uses CNN if available and image_data is provided, otherwise uses Random Forest if aspect_ratios are provided.

    Args:
        image_data (np.array, optional): Image data (NumPy array) for CNN.
        force_train (bool, optional): Force retraining of CNN (requires external data setup).
        aspect_ratios (dict, optional): Dictionary of aspect ratios for Random Forest.

    Returns:
        int: 1 if drowsy, 0 if active.

    Raises:
        ValueError: If insufficient inputs are provided for either method.
        FileNotFoundError: If the required model/data file is missing.
    """
    global USE_CNN, cnn_model_loaded, model # Allow modification if fallback occurs

    # --- CNN Prediction --- (Prioritized if image_data is available)
    if image_data is not None and USE_CNN:
        if not cnn_model_loaded and not force_train:
             # Check again if model exists before attempting prediction
             if not os.path.exists(get_cnn_model_path()):
                  print(f"Warning: CNN model file not found at {get_cnn_model_path()}. Cannot predict with CNN.")
             else:
                  cnn_model_loaded = True # Assume it exists now

        if cnn_model_loaded or force_train:
            try:
                # Pass image_data directly to the CNN prediction function
                # force_train might trigger training inside predict_drowsiness_with_cnn if needed
                prediction, confidence = predict_drowsiness_with_cnn(image_data=image_data, force_train=force_train)
                print(f"CNN prediction confidence: {confidence:.2f}")
                return prediction
            except FileNotFoundError as e:
                 print(f"CNN prediction failed: {e}. Model file might be missing.")
                 # Fall through to RF if possible
            except Exception as e:
                print(f"CNN prediction failed: {e}")
                # Fall through to RF if possible
        else:
             print("CNN method selected but model not available and force_train is False.")
             # Fall through to RF if possible

    # --- Random Forest Prediction --- (Used if CNN fails or aspect_ratios provided)
    if aspect_ratios is not None:
        if model is None:
            # Attempt to load RF model again if it wasn't loaded initially
            if dataset_path:
                print("Attempting to initialize Random Forest model on demand...")
                try:
                    dataframe = pd.read_csv(dataset_path)
                    X = dataframe.drop(columns=['drowsy'])
                    y = dataframe['drowsy']
                    # Note: Retraining RF model every time if not pre-loaded
                    # Consider saving/loading the trained RF model object (e.g., using joblib)
                    # For simplicity here, we retrain from CSV if needed.
                    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)
                    model = RandomForestClassifier(random_state=42, n_estimators=100)
                    model.fit(X_train, y_train)
                    print("Random Forest model initialized.")
                except Exception as rf_e:
                    raise RuntimeError(f"Failed to initialize Random Forest model on demand: {rf_e}")
            else:
                 raise RuntimeError("Random Forest model not available: dataset path not found.")
        elif model is None:\ # Check again after trying to load
             raise RuntimeError("Random Forest model is not available.")

        try:
            # Ensure all required keys are present
            required_keys = ['EAR', 'MAR', 'MOE', 'HPR', 'BAR']
            if not all(key in aspect_ratios for key in required_keys):
                raise ValueError(f"Missing required aspect ratios for Random Forest prediction. Need: {required_keys}")

            features = [[aspect_ratios[key] for key in required_keys]] # Order matters
            prediction = model.predict(features)
            print("Prediction using Random Forest.")
            return prediction[0]
        except Exception as e:
            raise RuntimeError(f"Random Forest prediction failed: {e}")

    # If neither method could run
    raise ValueError("Insufficient input: Provide image_data for CNN or aspect_ratios for Random Forest.")

# Keep the original function signature if it's used elsewhere, but maybe deprecate?
# def predict_drowsiness(EAR=None, MAR=None, MOE=None, HPR=None, BAR=None, image_path=None):
#     # This function is now less useful as the API takes image_data or path
#     # It could be adapted or removed.
#     print("Warning: Direct call to predict_drowsiness is deprecated. Use the main API function.")
#     ratios = None
#     img_data = None
#     if all(v is not None for v in [EAR, MAR, MOE, HPR, BAR]):
#         ratios = {'EAR': EAR, 'MAR': MAR, 'MOE': MOE, 'HPR': HPR, 'BAR': BAR}
#     if image_path:
#         import cv2
#         img_data = cv2.imread(image_path)
#         if img_data is None:
#              raise FileNotFoundError(f"Could not read image: {image_path}")
#     return predict_drowsiness_internal(image_data=img_data, aspect_ratios=ratios)