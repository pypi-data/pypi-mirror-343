from setuptools import setup, find_packages

setup(
    name="wandb_tsbw",
    version="0.1.0",
    packages=find_packages(),
    description="A compatibility layer for TensorBoard's SummaryWriter to log to Weights & Biases",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/wandb_tsbw",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    keywords="tensorflow, tensorboard, pytorch, wandb, logging, machine learning",
    install_requires=[
        "wandb>=0.12.0",
        "numpy>=1.19.0",
        "soundfile",
    ],
    python_requires=">=3.6",
)
