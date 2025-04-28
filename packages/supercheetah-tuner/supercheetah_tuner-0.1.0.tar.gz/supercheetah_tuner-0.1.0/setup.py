from setuptools import setup, find_packages

setup(
    name="supercheetah_tuner",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.20",
        "scikit-learn>=1.0",
    ],
    python_requires=">=3.7",
    author="Ujwal Watgule",
    description="Nature-inspired hyperparameter tuning with Cheetah optimizer",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/UjwalWtg/supercheetah-tuner",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)