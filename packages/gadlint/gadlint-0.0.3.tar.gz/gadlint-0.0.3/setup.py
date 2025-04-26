from setuptools import find_packages
from setuptools import setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="gadlint",
    version="0.0.3",
    packages=find_packages(),
    package_data={
        "gadlint": ["configs/*", "configs/.isort.cfg"],
    },
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "gadlint=gadlint.cli:app",
        ],
    },
    author="Alexander Grishchenko",
    author_email="alexanderdemure@gmail.com",
    description="CLI tool that runs isort, ruff, mypy, and radon with built-in configurations.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/AlexDemure/gadlint",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
