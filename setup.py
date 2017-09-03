"""Convert Spotify URLs to track info."""
from setuptools import setup

setup(
    name="spotify2csv",
    version="0.1.0",
    description="Convert Spotify URLs to tracks info in CSV format",
    license="MIT",
    keywords="convert spotify csv",
    python_requires=">=3",
    install_requires=[
        "beautifulsoup4",
        "progress",
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "spotify2csv=spotify2csv:main",
        ],
    },
)
