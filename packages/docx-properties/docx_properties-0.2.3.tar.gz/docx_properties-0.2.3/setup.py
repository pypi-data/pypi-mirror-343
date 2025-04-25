import platform
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Define base dependencies
install_requires = [
    "lxml>=4.5.0",
    "python-docx>=0.8.10",
]


setup(
    name="docx_properties",
    version="0.2.3",
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'docxprop=docx_properties.cli:main',
        ],
    },
    author="BegoByte",
    description="Library for reading and editing properties in Word documents",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BegoByte/docx_properties",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)