from setuptools import setup, find_packages

setup(
    name="HandTrackingSheerin",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "opencv-python",
        "mediapipe"
    ],
    author="Sheerin",
    author_email="sheerinsultana96@gmail.com",
    description="Simple Hand Tracking Module using OpenCV and MediaPipe",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/SheerinIbrahim/PythonPackages/tree/b08585c8a453c12566efb51cae02412d45175f7c/handtrackingmodule",  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
)
