from setuptools import setup, find_packages

setup(
    name="ffmpeg-ai",  # PyPI name (hyphens allowed)
    version="0.1.1",   # 🔥 (remember to bump version if reuploading)
    description="AI-powered FFmpeg command generator",
    author="Aliasgar Jiwani",
    author_email="aliasgarjiwani@gmail.com",
    url="https://github.com/Aliasgar-Jiwani/ffmpeg-ai",
    packages=["ffmpeg_ai"],  # module name: must be underscore
    package_dir={"ffmpeg_ai": "src/ffmpeg_ai"},  # 🔥 correct mapping with underscores
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
            "ffmpeg-ai=ffmpeg_ai.cli:app",  # command-line alias
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
