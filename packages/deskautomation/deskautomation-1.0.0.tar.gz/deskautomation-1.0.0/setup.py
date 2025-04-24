from setuptools import setup, find_packages

setup(
    name="Deskautomation",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pyautogui",
        "opencv-python",
        "pillow",
        "numpy",
        "pygetwindow",
        "pytesseract"
    ],
    author="Mehabalan",
    author_email="majesticmehabalan@email.com",
    description="Custom Robot Framework library for desktop automation",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    keywords=["robotframework", "automation", "desktop", "pyautogui", "ocr"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ],
)
