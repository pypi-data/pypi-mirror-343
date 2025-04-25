from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="e164_python_sdk",  # Changed from e164-python-sdk to comply with PEP 625
    version="0.1.5",
    description="A Python SDK package for accessing the e164.com phone number validation API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Catalin Dragos",
    author_email="catalin.dragos@e164.com",
    url="https://github.com/e164-com/e164-python-sdk",  # Replace with your GitHub repo URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=["requests"],  # Add dependencies here
)
