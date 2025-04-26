from setuptools import setup, find_packages

setup(
    name="iCompress",
    version="0.1.0",
    author="Rahul Rathod",
    author_email="rahul.rathod@gmail.com",
    description="A Python package for text compression using Huffman coding.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/rahulrathod315/iCompress-The-File-Compressor/",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
