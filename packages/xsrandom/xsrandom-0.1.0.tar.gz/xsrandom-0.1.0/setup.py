from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="xsrandom",
    version="0.1.0",
    author="XasdesNew",
    author_email="xasdesnew@gmail.com",
    description="Расширенная библиотека для генерации случайных значений в Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/XasdesXX/xsrandom",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
    install_requires=[
        "numpy>=1.19.0",
    ],
    keywords="random, randomization, generator, statistics, distribution, stochastic",
) 