from setuptools import setup, find_packages

with open("readme.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="anti-profanity",
    version="0.1.3",
    author="MeeRazi",
    description="A multilingual profanity filter supporting English, Hindi, and Bengali",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MeeRazi/anti-profanity",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Text Processing :: Filters",
        "Natural Language :: English",
    ],
    python_requires=">=3.6",
    include_package_data=True,
    package_data={
        "anti-profanity": ["data/*.py"],
    },
)