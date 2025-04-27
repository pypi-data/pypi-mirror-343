from setuptools import setup, find_packages

setup(
    name="hellimath",  # Library name
    version="1.0.0",
    author="steam",
    description="A powerful mathematical library for Python",
    
    # Improved long_description handling
    long_description=open("README.md", encoding="utf-8").read() if "README.md" in __import__("os").listdir() else "A powerful mathematical library for Python.",
    long_description_content_type="text/markdown",

    packages=find_packages(),
    install_requires=[
        "numpy",
        "scipy",
        "sympy",
        "statistics"
    ],
    
    # Additional metadata
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Mathematics"
    ],

    # Improved Python version requirement
    python_requires=">=3.7",
)