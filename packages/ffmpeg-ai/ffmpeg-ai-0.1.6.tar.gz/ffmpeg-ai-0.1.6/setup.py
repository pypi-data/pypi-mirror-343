from setuptools import setup, find_packages

# Read the contents of README.md
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="ffmpeg-ai",
    version="0.1.6",
    description="AI-powered FFmpeg command generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Aliasgar Jiwani",
    author_email="aliasgarjiwani@gmail.com",
    url="https://github.com/Aliasgar-Jiwani/ffmpeg-ai",
    packages=find_packages(where="src"),  # Automatically finds packages inside 'src'
    package_dir={"": "src"},  # Maps the root to 'src'
    install_requires=[
        "typer",
        "rich",
        "langchain",
        "ollama",
        "chromadb",
        "requests",
        "beautifulsoup4",
        "html2text",
        "langchain-huggingface",
    ],
    entry_points={
        "console_scripts": [
            "ffmpeg-ai=ffmpeg_ai.cli:app",  # Points to your main CLI entry point
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
