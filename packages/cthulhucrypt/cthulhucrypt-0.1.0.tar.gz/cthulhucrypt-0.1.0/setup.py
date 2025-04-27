from setuptools import setup, find_packages

setup(
    name="cthulhucrypt",
    version="0.1.0",
    packages=find_packages(),
    description="An unholy encryption algorithm that defies brute force",
    author="null",
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "cthulhucrypt=cthulhucrypt.cli:cli"
        ],
    }
)