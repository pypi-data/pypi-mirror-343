from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="noir-llm",
    version="0.2.2",
    author="Noir Team",
    author_email="noir.llm.team@gmail.com",
    description="A Python package for accessing various LLM models freely",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/noir-llm/noir",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
        "colorama>=0.4.4",
    ],
    entry_points={
        "console_scripts": [
            "noir-llm=noir.cli:main",
        ],
    },
)
