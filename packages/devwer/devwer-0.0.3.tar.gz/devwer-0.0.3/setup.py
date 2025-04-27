from setuptools import setup, find_packages

setup(
    name="devwer",
    version="0.0.3",
    description="A Word Error Rate (WER) evaluation Metrics Calculator for Devnagari (Nepali) language.",
    author="Kiran Pantha",
    author_email="info@kiranpantha.com.np",
    url="https://github.com/kiranpantha/DevWordErrorRate",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "numpy>=1.18.0",
        "python-Levenshtein"
    ],
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",  # or "text/x-rst" if using reStructuredText
)