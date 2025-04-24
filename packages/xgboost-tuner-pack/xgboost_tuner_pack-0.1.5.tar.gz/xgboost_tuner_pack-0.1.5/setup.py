import os
from setuptools import setup, find_packages

def read(fname: str) -> str:
    """Read and return the contents of the given file."""
    here = os.path.dirname(__file__)
    path = os.path.join(here, fname)
    with open(path, encoding="utf-8") as f:
        return f.read()

setup(
    name="xgboost-tuner-pack",  # Your PyPI package name
    version="0.1.5",
    author="Aroop",
    author_email="work.arooprath@gmail.com",
    description="A hyperparameter tuner for XGBoost.",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/AroopGit/XGB_Tuner",
    packages=find_packages(),
    install_requires=[
        "xgboost>=1.0",
        "scikit-learn>=1.0",
        "numpy>=1.17",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            # syntax: script-name = module.path:function
            "xgbtuner = xgbtuner.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="xgboost tuner hyperparameter optimization",
)
