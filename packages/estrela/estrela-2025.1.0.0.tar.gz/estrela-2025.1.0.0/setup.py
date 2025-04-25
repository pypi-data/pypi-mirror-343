# setup.py

from setuptools import setup

setup(
    name="estrela",
    version="2025.1.0.0",
    description="Uma biblioteca de exemplo simples para ensino",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="maria eduarda",
    author_email="mariaeduarda.e.m32360824@gmai.com",
    url="https://github.com/xxxxx/dobro",
    packages=['dobro'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        'Natural Language :: Portuguese (Brazilian)',
    ],
    python_requires=">=3.6",
)