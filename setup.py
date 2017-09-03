"""Spotify2CSV setup."""

from setuptools import setup

with open("README.rst") as f:
    LONG_DESCRIPTION = f.read()

setup(
    name="spotify2csv",
    version="0.1.0",
    python_requires=">=3",
    author="Arthur White",
    author_email="arthur@white.li",
    license="MIT",
    description="Convert Spotify URLs to tracks info in CSV format",
    long_description=LONG_DESCRIPTION,
    keywords="convert spotify csv",
    url="https://github.com/arthurwhite/spotify2csv",
    classifiers=[
        "Development Status :: 5 - Production/Stable"
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Utilities",
    ],
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
