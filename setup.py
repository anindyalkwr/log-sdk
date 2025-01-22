from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="log-sdk",
    version="0.1.0",
    author="Anindya Lokeswara",
    author_email="lokeswaraanindya@gmail.com",
    description="A standardized logging SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/anindyalkwr/log-sdk",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)