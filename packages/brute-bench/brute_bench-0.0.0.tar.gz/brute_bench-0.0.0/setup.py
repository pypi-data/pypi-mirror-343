
from setuptools import setup, find_packages

setup(
    name="brute-bench",
    version="0.0.0",
    author="attentionmech",
    author_email="attentionmech@gmail.com",
    description="Placeholder package to reserve brute-bench on PyPI.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/brute-bench/",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 1 - Planning",
    ],
    python_requires='>=3.6',
)
