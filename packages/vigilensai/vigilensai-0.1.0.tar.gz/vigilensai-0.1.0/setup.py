from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="vigilensai",
    version="0.1.0",
    author="Rohit Joshi",
    author_email="joshi.rohit@yahoo.com",
    description="AI Safety & Monitoring Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/VigiLensAI",
    packages=find_packages(),
    install_requires=[
        "torch>=2.0.0",
        "transformers>=4.30.0",
        "datasets>=2.12.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)