from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Get the version from the version.py file
# This is a workaround to avoid circular imports
with open("bstokenizer/version.py", "r") as f:
    exec(f.read())

setup(
    name="bstokenizer",
    version=__version__,
    author="CodeSoft",
    author_email="hello@mail.codesoft.is-a.dev",
    description="A library for tokenizing Beat Saber maps and replays",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CodeSoftGit/bstokenizer",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "py-bsor", # For replay parsing
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov",
            "black",
        ],
    },
)