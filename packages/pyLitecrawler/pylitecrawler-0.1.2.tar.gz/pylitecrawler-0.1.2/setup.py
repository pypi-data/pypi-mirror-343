from setuptools import setup, find_packages

setup(
    name="pyLitecrawler",
    version="0.1.2",
    description="A lightweight Python library for scraping, crawling, and content analysis",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "selenium",
        "beautifulsoup4",
        "httpx",
        "requests",
        "fastapi"
    ],
    python_requires=">=3.8",
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

 