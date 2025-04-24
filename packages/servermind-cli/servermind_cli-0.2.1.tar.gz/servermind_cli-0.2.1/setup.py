from setuptools import setup, find_packages

setup(
    name="servermind_cli",
    version="0.2.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "openai",
        "python-dotenv",
        "rich",
        "click",
    ],
    entry_points={
        "console_scripts": [
            "servermind=servermind_cli.main:main",
        ],
    },
    author="ServerMind",
    author_email="support@servermind.ai",
    description="ServerMind CLI - AI-powered command line interface",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/servermind-cli",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
) 