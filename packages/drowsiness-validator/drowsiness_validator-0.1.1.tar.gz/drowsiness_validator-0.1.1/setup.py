# filepath: /Users/shazi/Desktop/projects/drowsiness-validator/setup.py
from setuptools import setup, find_packages
import os

# Function to read dependencies from requirements.txt
def read_requirements(file_path='requirements.txt'):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

# Read README for long description
try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "Drowsiness detection package using facial landmarks or CNN."

setup(
    name='drowsiness_validator',
    version='0.1.1', # Increment version for the new release
    author='Sharjeel Baig', 
    author_email='dr.sharjeel.6@gmail.com', 
    description='Drowsiness detection using facial landmarks or CNN.',
    long_description=long_description, # Use the README content
    long_description_content_type="text/markdown", # Specify markdown format
    url='https://github.com/yourusername/drowsiness-validator', # Replace with your repo URL
    packages=find_packages(include=['drowsiness_validator', 'drowsiness_validator.*']),
    install_requires=read_requirements(),
    package_data={
        'drowsiness_validator': [
            'modules/calculate/shape_predictor_68_face_landmarks.dat',
            'modules/predict/drowsiness_cnn_model.h5',
            # Add other necessary non-code files here
            # 'modules/predict/drowsiness_dataset.csv', # Include if needed at runtime
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License', 
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8', 
    # entry_points={
    #     'console_scripts': [
    #         'drowsiness-detect=drowsiness_validator.cli:main', # Optional CLI entry point
    #     ],
    # },
    include_package_data=True, 
)