from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="rearrange-pdf",
    version="0.1.2",
    author="htlin",
    author_email="your.email@example.com",
    description="A tool to rearrange PDF pages for printing booklets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/htlin222/rearrange-pdf.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "PyPDF2>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "rearrange-pdf=rearrange_pdf.cli:main",
        ],
    },
)
