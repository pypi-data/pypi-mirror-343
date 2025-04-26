from setuptools import setup, find_packages

setup(
    name="ffmpeg-ai",
    version="0.1.0",
    description="AI-powered FFmpeg command generator",
    author="Aliasgar Jiwani",
    author_email="aliasgarjiwani@gmail.com",
    url="https://github.com/Aliasgar-Jiwani/ffmpeg-ai",  # Optional: Link to your repository
    packages=find_packages(where="src"),
    package_dir={"": "src"},
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
            "ffmpeg-ai=ffmpeg_ai.cli:app",  # This makes your CLI accessible via `ffmpeg-ai`
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)