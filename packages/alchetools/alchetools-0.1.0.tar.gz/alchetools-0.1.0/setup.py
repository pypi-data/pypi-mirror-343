from setuptools import setup, find_packages

setup(
    name="alchetools",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A lightweight CRUD toolkit built on SQLAlchemy 2.x.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/alchetools",
    packages=find_packages(),
    install_requires=[
        "SQLAlchemy>=2.0.29"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)