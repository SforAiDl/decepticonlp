#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.md") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = []

setup_requirements = ["pytest-runner"]

test_requirements = ["pytest>=3"]

setup(
    author="Rajaswa Ravindra Patil",
    author_email="rajp4480@gmail.com",
    python_requires=">=3.5",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="Python package for Adversarial Debugging of Natural Language Models",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="decepticonlp",
    name="decepticonlp",
    packages=find_packages(include=["decepticonlp", "decepticonlp.*"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/SforAiDl/decepticonlp",
    version="0.1.0",
    zip_safe=False,
)
