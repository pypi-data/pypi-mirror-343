# filepath: /Users/shazi/Desktop/projects/drowsiness-validator/README.md

# Drowsiness Validator

A Python package for detecting drowsiness using facial landmarks or a Convolutional Neural Network (CNN).

## Installation

Install the package using pip:

```bash
pip install drowsiness-validator
```

## Usage

Here's a basic example of how to use the package:

```python
from drowsiness_validator import DrowsinessDetector
import cv2

# Initialize the detector (choose 'landmarks' or 'cnn')
detector = DrowsinessDetector(method='landmarks')
# Or: detector = DrowsinessDetector(method='cnn')

# Load an image (replace with your image path or video frame)
image_path = 'path/to/your/image.jpg'
frame = cv2.imread(image_path)

if frame is not None:
    # Detect drowsiness
    is_drowsy, details = detector.detect_drowsiness(frame)

    if is_drowsy:
        print("Drowsiness detected!")
        # You can access more details if needed, e.g., eye aspect ratio for landmarks
        if 'ear' in details:
            print(f"Eye Aspect Ratio (EAR): {details['ear']:.2f}")
    else:
        print("Not drowsy.")
else:
    print(f"Error loading image: {image_path}")

# Example with video stream (using OpenCV)
# cap = cv2.VideoCapture(0) # Use 0 for default webcam
# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break
#
#     is_drowsy, _ = detector.detect_drowsiness(frame)
#
#     status = "Drowsy" if is_drowsy else "Awake"
#     cv2.putText(frame, f"Status: {status}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255) if is_drowsy else (0, 255, 0), 2)
#
#     cv2.imshow("Drowsiness Detection", frame)
#
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# cap.release()
# cv2.destroyAllWindows()
```

_(Note: Ensure you have the necessary model files (`shape_predictor_68_face_landmarks.dat` for landmarks, `drowsiness_cnn_model.h5` for CNN) accessible by the package as defined in `setup.py`)_

## Author

Sharjeel Baig

- Portfolio: [https://sharjeelbaig.github.io](https://sharjeelbaig.github.io)
- GitHub: [https://github.com/yourusername/drowsiness-validator](https://github.com/yourusername/drowsiness-validator) _(Replace with your actual repo URL)_

## License

This project is licensed under the MIT License.
