from setuptools import setup, find_packages

setup(
    name="pseudo-runner",  # Name of the package
    version="0.1",         # Package version
    description="A tool to convert pseudocode to Python and execute it.",
    long_description=open("README.md").read(),  # Readme file for PyPI description
    long_description_content_type="text/markdown",
    author="Krishna Aggarwal",
    author_email="your-email@example.com",
    url="https://github.com/mrkrishnaaggarwal/pseudo-runner",  # Repo URL
    license="MIT",
    packages=find_packages(),  # Automatically find packages in your project
    install_requires=[
        "google-generativeai",  # Dependencies
        "python-dotenv",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",  # Minimum Python version
    entry_points={
        "console_scripts": [
            "pseudorun=pseudo_runner.cli:main",  # CLI entry point
        ],
    },
    include_package_data=True,  # Include data files like README, LICENSE
)