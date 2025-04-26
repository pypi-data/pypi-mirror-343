# setup.py
from setuptools import setup, find_packages
import pathlib # Import pathlib to read README

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
# Use encoding='utf-8' for broader compatibility
README = (HERE / "README.md").read_text(encoding='utf-8')

setup(
    name="xtnote",  # The name you want people to use for pip install
    version="0.1.0", # Start with a version number
    description="A simple command-line note-taking tool",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/xtnote", # <--- Replace with your GitHub URL
    author="Your Name", # <--- Replace with your name
    author_email="your.email@example.com", # <--- Replace with your email
    license="MIT", # Or choose another license (e.g., Apache 2.0)
    classifiers=[
        "Development Status :: 3 - Alpha", # Choose appropriate status
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License", # If using MIT
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6", # Specify supported versions
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: Text Editors",
        "Topic :: Utilities",
    ],
    package_dir={'': 'src'}, # Tell setuptools that packages are under src/
    packages=find_packages(where='src'), # Automatically find packages in src/
    include_package_data=True, # If you have non-code data files (like README, LICENSE)
    install_requires=[ # List your dependencies here
        "rich",
        "questionary",
        # pathlib is built-in
        # subprocess is built-in
        # shutil is built-in
    ],
    python_requires=">=3.6", # Minimum Python version required
    entry_points={
        # This is the key part for creating the command line tool
        # 'xtnote' is the command users will type
        # 'xtnote.cli' refers to the cli.py file inside the xtnote package (src/xtnote/cli.py)
        # ':main_menu' refers to the main_menu function within cli.py
        'console_scripts': [
            'xtnote = xtnote.cli:main_menu',
        ],
    },
)

