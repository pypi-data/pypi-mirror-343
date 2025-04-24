from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="openinterest",
    version="0.1.1",
    author="Charles Verge",
    author_email="charles.v@charlesverge.com",
    description="Calculate max pain from open interest data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/charlesverge/openinterest",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",
    install_requires=[
        "numpy>=1.20.0",
        "pandas==2.2.1",
        "pandas_market_calendars==4.6.1",
    ],
)
