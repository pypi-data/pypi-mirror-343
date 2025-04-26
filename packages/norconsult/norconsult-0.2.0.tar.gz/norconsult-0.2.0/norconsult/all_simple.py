[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "norconsult-utilities"
version = "0.1.0"
authors = [
  { name="Bhupan", email="bhuwanpanday1@gmail.com" },
]
description = "A collection of utility functions related to Norconsult work."
readme = "README.md"
requires-python = ">=3.8"
license = {text = "MIT License"}
keywords = ["norconsult", "utilities", "sosi", "calculations", "pandas", "scipy"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Operating System :: OS Independent",
    "Topic :: Software Development :: Libraries :: Python Modules",
]
dependencies = [
    "pandas",
    "chardet",
    "scipy",
]

[project.urls]
"Homepage" = "https://github.com/BHUWANPANDY/Utillities"
"Bug Tracker" = "https://github.com/BHUWANPANDY/Utillities/issues"

[tool.setuptools.packages.find]
where = ["src"]
