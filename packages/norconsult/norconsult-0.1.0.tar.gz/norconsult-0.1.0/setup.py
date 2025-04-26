import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="norconsult",
    version="0.1.0",
    author="Bhuwan Panday",
    author_email="bhuwanpanday@example.com",  # Replace with your actual email
    description="A set of calculation utilities for Norconsult",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bhuwanpanday/Norconsult",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)