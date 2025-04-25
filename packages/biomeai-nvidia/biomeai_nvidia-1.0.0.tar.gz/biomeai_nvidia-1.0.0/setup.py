from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="biomeai-nvidia",
    version="1.0.0",
    author="The Raj",
    author_email="theraj05@duck.com",
    description="A package for easy integration with NVIDIA AI capabilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TheRaj71",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "httpx>=0.24.0",
        "typing-extensions>=4.0.0",
        "python-dotenv>=0.19.0"
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-asyncio>=0.20.0',
            'pytest-cov>=4.0.0'
        ]
    },
)
