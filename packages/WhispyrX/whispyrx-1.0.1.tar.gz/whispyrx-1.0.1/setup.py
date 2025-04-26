from setuptools import setup, find_packages
from pathlib import Path

# Read the content of README.md
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="WhispyrX",
    version="1.0.1",
    description="A peer-to-peer TUI chat app using Textual",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="MOHAMMAD SHAHARIAR AHMMED SHOVON",
    author_email="shovonali885@proton.me",
    url="https://pypi.org/project/WhispyrX/",
    packages=find_packages(),
    install_requires=[
        "textual",
        "httpx",
        "requests",
        "sseclient",
        "emoji"
    ],
    entry_points={
        "console_scripts": [
            "whispyrx=whispyrx.app:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Topic :: Communications :: Chat",
    ],
    python_requires=">=3.9",
)
