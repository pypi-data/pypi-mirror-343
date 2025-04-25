from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="anti-profanity",
    version="0.2.0",
    author="MeeRazi",
    description="A multilingual profanity filter supporting English, Hindi, and Bengali",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MeeRazi/anti-profanity",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Text Processing :: Filters",
        "Natural Language :: English",
    ],
    python_requires=">=3.6",
    package_data={
        "anti_profanity": ["data/*.py"],
    },
    include_package_data=True,
)