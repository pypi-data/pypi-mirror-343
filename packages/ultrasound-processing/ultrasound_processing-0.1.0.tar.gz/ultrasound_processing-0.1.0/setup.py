from setuptools import setup, find_packages

setup(
    name="ultrasound_processing",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "matplotlib",
        "opencv-python",
        "scipy",
        "Pillow"
    ],
    author="A Te Neved",
    description="Ultrahang képfeldolgozó csomag",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Mart-SciecPyt/ScPytone_ultrasound_processing",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
