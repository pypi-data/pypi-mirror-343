from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="nultack",
    version="1.8.0",
    author="Eternals-Satya",
    author_email="eternals.tolong@gmail.com",
    description="Nültack - Python Code Steganography Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Eternals-Satya/Nultack",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    keywords="steganography, obfuscation, python, security",
)
