# setup.py
from setuptools import setup, find_packages

setup(
    name="yandex-book-api",
    version="0.1.0",
    description="Pydantic wrapper for Bookmate API",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="you@example.com",
    license="MIT",
    url="https://github.com/yourusername/yandex-book-api",
    packages=find_packages(exclude=["tests*"]),
    install_requires=[
        "pydantic>=2.0",
        "requests>=2.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
