from setuptools import setup, find_packages

setup(
    name="vibeshub-core",
    version="0.2.0",
    description="Core utility functions for the VibesHub ecosystem.",
    author="Iliyan Slavchov",
    author_email="yani.slavchov@gmail.com",
    url="https://github.com/vibeshub-org/vibeshub-core",
    packages=find_packages(),
    install_requires=[],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
