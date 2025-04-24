from setuptools import setup, find_packages

setup(
    name="orofacIAnalysis",
    use_scm_version=True,
    setup_requires=['setuptools>=42', 'setuptools-scm'],
    packages=find_packages(),
    install_requires=[
        "numpy>=1.20.0",
        "opencv-python>=4.5.0",
        "mediapipe>=0.8.10",
        "scipy>=1.7.0",
        "pandas>=1.3.0", 
        "matplotlib>=3.4.0",
        "PyEMD>=0.2.0",
        "statsmodels>=0.13.0",
    ],
    author="Cameron Maloney",
    author_email="cameron.maloney@warriorlife.net",
    description="A library for analyzing chewing patterns using computer vision",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/orofacIAnalysis",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
