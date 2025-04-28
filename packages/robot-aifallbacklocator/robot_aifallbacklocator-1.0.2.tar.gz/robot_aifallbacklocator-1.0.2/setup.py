#!/usr/bin/env python3

from setuptools import setup, find_packages
import os

with open(os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="robot_aifallbacklocator",
    version="1.0.2",
    packages=find_packages(),
    py_modules=["DomRetryLibrary", "AIFallbackLocator"],
    install_requires=[
        "robotframework>=4.0.0",
        "python-dotenv>=0.19.0",
        "requests>=2.25.0",
    ],
    include_package_data=True,
    description="AI-powered smart locator with retry functionality for Robot Framework using OpenAI",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Kristijan Plaushku',
    author_email='info@plaushkusolutions.com',
    url='https://github.com/plaushku/robotframework-domretrylibrary',
    python_requires='>=3.7',
    classifiers=[
        'Framework :: Robot Framework',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
    ],
) 