"""
AMGD package setup script.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="amgd",
    version="0.1.0",
    author="Ibrahim Bakari",
    author_email="acbrhmbakari@gmail.com",
    description="Adaptive Momentum Gradient Descent (AMGD) for Penalized Poisson Regression",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/elbakari01/amgd-Poisson-regression",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    python_requires=">=3.6",
    install_requires=[
        "numpy>=1.18.0",
        "scipy>=1.4.0",
        "matplotlib>=3.1.0",
        "scikit-learn>=0.22.0",
        "pandas>=1.0.0",
        "seaborn>=0.10.0",
    ],
)