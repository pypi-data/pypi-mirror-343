from setuptools import setup, find_packages
import os

# Read version from package
def get_version():
    with open("biascheck/__init__.py", "r") as f:
        for line in f:
            if line.startswith("__version__"):
                return line.split("=")[1].strip().strip('"')
    raise RuntimeError("Unable to find version string.")

# Read README.md for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="biascheck",
    version=get_version(),
    author="Arjun Balaji",
    author_email="",
    description="A library for detecting and analyzing bias in text, datasets, and language models.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-repo/biascheck",
    packages=find_packages(),
    python_requires=">=3.9,<3.11",
    install_requires=[
        # Core dependencies
        "numpy",
        "torch",
        "transformers",
        "pandas",
        "scikit-learn",
        "scipy",
        
        # NLP and text processing
        "spacy",
        "textblob",
        "sentence-transformers",
        
        # Visualization
        "matplotlib",
        "seaborn",
        "wordcloud",
        
        # PDF processing
        "PyPDF2",
        "PyMuPDF",
        
        # Vector storage
        "faiss-cpu",
        
        # LangChain ecosystem
        "langchain",
        "langchain-community",
        "langchain_huggingface",
        "langchain_ollama",
        
        # Graph database
        "py2neo",
        
        # Datasets
        "datasets"
    ],
    extras_require={
        "test": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
    ],
    entry_points={
        "console_scripts": [
            "biascheck=biascheck.cli:main",
        ],
    },
    include_package_data=True,
)