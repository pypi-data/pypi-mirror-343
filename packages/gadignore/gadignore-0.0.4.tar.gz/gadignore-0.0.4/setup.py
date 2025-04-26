from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="gadignore",
    version="0.0.4",
    packages=find_packages(),
    package_data={
        "gadignore": [".gitignore"],
    },
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "gadignore=gadignore.cli:app",
        ],
    },
    author="Alexander Grishchenko",
    author_email="alexanderdemure@gmail.com",
    description="CLI tool for quickly generating a .gitignore file for Python projects",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/AlexDemure/gadignore",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)