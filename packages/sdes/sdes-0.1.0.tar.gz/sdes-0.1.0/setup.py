from setuptools import setup, find_packages

setup(
    name="sdes",  # The name of your package
    version="0.1.0",  # Initial release version
    packages=find_packages(),
    install_requires=[
        "bitarray",  # Add any dependencies your package has
    ],
    description="Simplified Data Encryption Standard (S-DES) Implementation",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Your Name",
    author_email="your.email@example.com",
    license="MIT",  # Choose an open-source license
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
