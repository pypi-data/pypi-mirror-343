from setuptools import setup, find_packages

setup(
    name="WhispyrX",
    version="1.0.0",
    description="A peer-to-peer TUI chat app using Textual",
    author="MOHAMMAD SHAHARIAR AHMMED SHOVON",
    author_email="shovonali885@proton.me",
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
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
