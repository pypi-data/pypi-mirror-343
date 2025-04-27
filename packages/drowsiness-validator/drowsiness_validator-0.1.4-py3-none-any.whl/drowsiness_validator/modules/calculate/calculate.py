import cv2
import dlib
import numpy as np
from scipy.spatial import distance as dist
import pandas as pd # Import pandas
import os
import pkg_resources # Use pkg_resources to find data files

# Function to get the path to the data file within the package
def get_predictor_path():
    # Use pkg_resources to find the path relative to the package
    try:
        # Adjust the resource path based on the structure defined in setup.py
        predictor_path = pkg_resources.resource_filename('drowsiness_validator', 'modules/calculate/shape_predictor_68_face_landmarks.dat')
    except Exception as e:
        # Fallback or error handling if the resource isn't found
        print(f"Error finding predictor data file: {e}")
        # Attempt a relative path as a fallback (might work during development)
        predictor_path = os.path.join(os.path.dirname(__file__), 'shape_predictor_68_face_landmarks.dat')
        if not os.path.exists(predictor_path):
             raise FileNotFoundError("Could not find shape_predictor_68_face_landmarks.dat")
    return predictor_path

# Load Dlib models
face_detector = dlib.get_frontal_face_detector()
# Load the predictor using the helper function
landmark_predictor = dlib.shape_predictor(get_predictor_path())

def compute_ear(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

def compute_mar(mouth):
    A = dist.euclidean(mouth[3], mouth[7])
    B = dist.euclidean(mouth[4], mouth[6])
    C = dist.euclidean(mouth[2], mouth[6])
    D = dist.euclidean(mouth[1], mouth[5])
    mar = (A + B + C) / (2.0 * D)
    return mar

def compute_hpr(nose_chin, nose_forehead):
    return nose_chin / nose_forehead

def compute_bar(brow_points, eye_points):
    vertical_distances = [abs(brow[1] - eye[1]) for brow, eye in zip(brow_points, eye_points)]
    return np.mean(vertical_distances)

def extract_landmarks(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_detector(gray)

    if len(faces) == 0:
        raise Exception("No face detected!")

    face = faces[0]
    shape = landmark_predictor(gray, face)
    coords = np.array([[p.x, p.y] for p in shape.parts()])
    return coords

def calculate_all_ARs(image_path=None, image_data=None):
    """Calculates all aspect ratios from either an image path or image data (numpy array)."""
    if image_path:
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Could not read image from path: {image_path}")
    elif image_data is not None:
        image = image_data # Use the provided numpy array
    else:
        raise ValueError("Either image_path or image_data must be provided.")

    landmarks = extract_landmarks(image)

    # Eye landmarks
    left_eye = landmarks[42:48]
    right_eye = landmarks[36:42]

    # Mouth landmarks (inner mouth)
    inner_mouth = landmarks[60:68]

    # Nose to chin / forehead for HPR
    nose_tip = landmarks[30]
    chin = landmarks[8]
    forehead = landmarks[27]

    # Brow and Eye center points for BAR
    brow_right = landmarks[22:27]  # Right brow
    eye_right = landmarks[42:48]   # Right eye

    # Compute ARs
    ear_left = compute_ear(left_eye)
    ear_right = compute_ear(right_eye)
    ear = (ear_left + ear_right) / 2.0

    mar = compute_mar(inner_mouth)
    # Avoid division by zero if ear is zero
    moe = mar / ear if ear != 0 else float('inf')

    nose_chin_dist = dist.euclidean(nose_tip, chin)
    nose_forehead_dist = dist.euclidean(nose_tip, forehead)
    # Avoid division by zero if forehead distance is zero
    hpr = compute_hpr(nose_chin_dist, nose_forehead_dist) if nose_forehead_dist != 0 else float('inf')

    bar = compute_bar(brow_right, eye_right[:5])  # Match 5 points

    return {
        "EAR": round(ear, 4),
        "MAR": round(mar, 4),
        "MOE": round(moe, 4),
        "HPR": round(hpr, 4),
        "BAR": round(bar, 4)
    }

# Keep calculate_ARs as a wrapper if needed, or remove if calculate_all_ARs is sufficient
def calculate_ARs(image_path=None, image_data=None):
    try:
        ar_values = calculate_all_ARs(image_path=image_path, image_data=image_data)
        return ar_values
    except Exception as e:
        print(f"Error calculating ARs: {e}")
        # Return a dictionary indicating error, or re-raise
        return {"error": str(e)}

# Example usage (commented out for package use)
# if __name__ == "__main__":
#     # Example using path
#     # image_path_test = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'images.jpeg') # Adjust path relative to this file
#     # ar_values = calculate_all_ARs(image_path=image_path_test)
#     # df = pd.DataFrame([ar_values])
#     # print(df)

#     # Example using image data (if you load it elsewhere)
#     # img = cv2.imread(image_path_test)
#     # if img is not None:
#     #     ar_values_data = calculate_all_ARs(image_data=img)
#     #     df_data = pd.DataFrame([ar_values_data])
#     #     print("From data:", df_data)
#     pass
