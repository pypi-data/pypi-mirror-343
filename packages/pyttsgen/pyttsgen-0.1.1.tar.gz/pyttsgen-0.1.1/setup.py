from setuptools import setup, find_packages
from pathlib import Path

# Dynamically read version from pyttsgen/__init__.py
def get_version():
    version_file = Path("pyttsgen/__init__.py").read_text(encoding="utf-8")
    for line in version_file.splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")

# Load README.md
long_description = Path("README.md").read_text(encoding="utf-8")

setup(
    name="pyttsgen",
    version=get_version(),  # ← Dynamically used here
    description="A developer-friendly, plug-and-play TTS library for Python supporting multiple outputs and integrations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="RePromptsQuest",
    author_email="repromptsquest@gmail.com",
    packages=find_packages(),
    install_requires=[
        "edge_tts",
        "streamlit",
        "nest_asyncio"
    ],
    entry_points={
        "console_scripts": [
            "pyttsgen=pyttsgen.cli:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
