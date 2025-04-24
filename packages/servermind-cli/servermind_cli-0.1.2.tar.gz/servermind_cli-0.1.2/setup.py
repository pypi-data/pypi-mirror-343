from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="servermind-cli",
    version="0.1.2",
    author="ServerMind",
    author_email="support@servermind.ai",
    description="ServerMind CLI Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/servermind/cli-cursor",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "servermind=servermind_cli.main:main",
        ],
    },
    include_package_data=True,
) 