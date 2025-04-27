import base64
import io
import os
import sys
import tempfile
import numpy as np
from PIL import Image
import cv2 # Import cv2 here as it's likely needed for image processing

# Use relative imports within the package
from .modules.calculate.calculate import calculate_all_ARs
# Import the internal prediction function from predict.py
from .modules.predict.predict import predict_drowsiness_internal

def detect_drowsiness(image_path=None, image_base64=None, method='cnn', force_train_cnn=False, train_dir=None, test_dir=None):
    """
    Detects drowsiness from an image using either CNN or facial aspect ratios (via Random Forest).

    Args:
        image_path (str, optional): Path to the input image file. Defaults to None.
        image_base64 (str, optional): Base64 encoded string of the input image. Defaults to None.
        method (str, optional): Method for detection ('cnn' or 'aspect_ratio'). Defaults to 'cnn'.
        force_train_cnn (bool, optional): Whether to force retraining of the CNN model.
                                         Requires train_dir and test_dir to be set.
                                         Defaults to False.
        train_dir (str, optional): Path to the training data directory (needed if force_train_cnn=True).
        test_dir (str, optional): Path to the test data directory (needed if force_train_cnn=True).

    Returns:
        dict: A dictionary containing the prediction result and method used.
              Example: {'prediction': 1, 'status': 'Drowsy', 'method': 'cnn'}
                       {'prediction': 0, 'status': 'Active', 'method': 'aspect_ratio', 'ratios': {...}}
                       {'error': 'Error message'}

    Raises:
        ValueError: If neither image_path nor image_base64 is provided, or if both are provided.
        FileNotFoundError: If the provided image_path does not exist.
        Exception: For other processing errors (e.g., face detection failure, model errors).
    """
    if not image_path and not image_base64:
        raise ValueError("Either image_path or image_base64 must be provided.")
    if image_path and image_base64:
        raise ValueError("Provide either image_path or image_base64, not both.")

    img_array = None
    temp_image_to_delete = None # Keep track if we created a temp file from base64

    try:
        # --- Image Loading --- 
        if image_base64:
            try:
                image_data = base64.b64decode(image_base64)
                image = Image.open(io.BytesIO(image_data))
                # Convert PIL Image to OpenCV format (numpy array BGR)
                img_array = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            except Exception as e:
                return {'error': f"Error decoding/loading base64 image: {e}"}
        elif image_path:
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image path does not exist: {image_path}")
            img_array = cv2.imread(image_path)
            if img_array is None:
                 return {'error': f"Error reading image file: {image_path}"}

        if img_array is None:
             return {'error': "Failed to load image data."}

        # --- Prediction Logic --- 
        prediction = None
        result_data = {}

        if method == 'aspect_ratio':
            # 1. Calculate aspect ratios
            aspect_ratios = calculate_all_ARs(image_data=img_array)
            if 'error' in aspect_ratios:
                 # Propagate error from calculation (e.g., no face detected)
                 return {'error': f"Aspect ratio calculation failed: {aspect_ratios['error']}"}

            # 2. Predict using the internal function (which uses Random Forest if configured)
            try:
                prediction = predict_drowsiness_internal(aspect_ratios=aspect_ratios)
                result_data['ratios'] = aspect_ratios
            except (RuntimeError, ValueError) as e:
                 return {'error': f"Aspect ratio prediction failed: {e}"}

        elif method == 'cnn':
            # Predict using the internal function (which uses CNN)
            try:
                # Pass necessary args for potential training
                prediction = predict_drowsiness_internal(image_data=img_array,
                                                         force_train=force_train_cnn,
                                                         train_dir=train_dir, # predict_internal might not use these directly
                                                         test_dir=test_dir)   # but cnn_model.predict_drowsiness_with_cnn does
            except (FileNotFoundError, ValueError, RuntimeError) as e:
                 return {'error': f"CNN prediction failed: {e}"}
        else:
            return {'error': f"Invalid method specified: {method}. Choose 'cnn' or 'aspect_ratio'."}

        # --- Format Output --- 
        if prediction is not None:
            status = 'Drowsy' if prediction == 1 else 'Active'
            result_data.update({
                'prediction': prediction,
                'status': status,
                'method': method
            })
            return result_data
        else:
            # Should not happen if methods are valid, but as a safeguard
            return {'error': "Prediction could not be determined."}

    except Exception as e:
        # Catch-all for unexpected errors during processing
        return {'error': f"An unexpected error occurred: {e}"}
    finally:
        # Clean up temporary file if one was created (though current logic uses img_array directly)
        # If calculate_all_ARs needed a path from base64, cleanup would be here.
        pass

# Example usage (commented out for package use)
# if __name__ == '__main__':
#     # Example with image path (relative to project root)
#     # Ensure the test image exists at the root or adjust path
#     test_img_path = '../images.jpeg'
#     if os.path.exists(test_img_path):
#         result_path_cnn = detect_drowsiness(image_path=test_img_path, method='cnn')
#         print(f"CNN Path Result: {result_path_cnn}")
#         result_path_ar = detect_drowsiness(image_path=test_img_path, method='aspect_ratio')
#         print(f"AR Path Result: {result_path_ar}")
#     else:
#         print(f"Test image not found: {test_img_path}")

#     # Example with base64
#     try:
#         if os.path.exists(test_img_path):
#             with open(test_img_path, 'rb') as f:
#                 img_b64 = base64.b64encode(f.read()).decode('utf-8')
#             result_b64_cnn = detect_drowsiness(image_base64=img_b64, method='cnn')
#             print(f"CNN Base64 Result: {result_b64_cnn}")
#             result_b64_ar = detect_drowsiness(image_base64=img_b64, method='aspect_ratio')
#             print(f"AR Base64 Result: {result_b64_ar}")
#         else:
#             print(f"Test image not found for base64 example: {test_img_path}")
#     except Exception as e:
#         print(f"Error in base64 example: {e}")
