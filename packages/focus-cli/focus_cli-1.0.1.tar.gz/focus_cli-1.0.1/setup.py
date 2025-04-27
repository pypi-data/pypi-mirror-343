from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")


setup(
    name="focus-cli",
    version="1.0.1",
    description="A powerful CLI tool for developers to boost productivity with tasks, sprints, goals, and notes management.",
    long_description=long_description,  # Use the UTF-8 version!
    long_description_content_type="text/markdown",
    author="PyGen Labs",
    author_email="pygen.co@gmail.com",
    url="https://github.com/pygen-labs/focus-cli",
    packages=find_packages(exclude=["tests", "tests.*"]),
    package_data={
        "focus_cli": ["data/*.json"],
    },
    include_package_data=True,
    install_requires=[
        "click>=8.0.0",
        "colorama>=0.4.4",  # For colored terminal output
        "tabulate>=0.8.9",  # For formatting tables in terminal
        "python-dateutil>=2.8.2",  # For date handling
        "tqdm>=4.65.0",  # For progress bars in sprints
        "rich>=10.0.0",  # For rich terminal formatting
    ],
    entry_points={
        "console_scripts": [
            "focus=focus_cli.cli:main",  # Updated import path
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Utilities",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    keywords="productivity, cli, developer-tools, task-management, pomodoro, goals",
    project_urls={
        "Bug Reports": "https://github.com/pygen-labs/focus-cli/issues",
        "Source": "https://github.com/pygen-labs/focus-cli",
        "Documentation": "https://github.com/pygen-labs/focus-cli#readme",
    },
)