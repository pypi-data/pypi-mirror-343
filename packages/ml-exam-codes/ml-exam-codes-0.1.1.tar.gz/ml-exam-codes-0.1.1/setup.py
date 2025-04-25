from setuptools import setup, find_packages

setup(
    name="ml-exam-codes",
    version="0.1.1",  # Fixed from "0.1."
    author="Your Name",
    author_email="your.email@example.com",
    description="A library containing ML code snippets for exam preparation",
    
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ml_exam_codes",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)