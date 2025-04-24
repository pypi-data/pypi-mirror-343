
from setuptools import setup, find_packages

setup(
    name='deskautomation',
    version='1.0.3',
    description='A library for desktop automation using PyAutoGUI and OCR.',
    author='Mehabalan',
    author_email='majesticmehabalan@gmail.com',
    packages=find_packages(),
    install_requires=[
        'pyautogui',
        'pytesseract',
        'pygetwindow',
        'Pillow',
        'opencv-python',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
