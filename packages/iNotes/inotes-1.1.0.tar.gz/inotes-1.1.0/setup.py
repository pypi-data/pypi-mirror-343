from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    description = f.read()

setup(
    name="iNotes",
    version="1.1.0",
    packages=find_packages(),
    install_requires=[
        "reportlab",
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "iNotes=iNotes.__main__:main",
        ],
    },
    long_description=description,
    long_description_content_type="text/markdown",
    author="TejusDubey",
    license="MIT",
)