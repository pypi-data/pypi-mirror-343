from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="urlify-simple",  
    version="0.1.1",
    author="The Raj",
    author_email="theraj05@duck.com",
    description="A simple URL shortener package using TinyURL",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TheRaj71",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.1",
    ],
)
