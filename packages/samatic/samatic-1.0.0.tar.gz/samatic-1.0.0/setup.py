import setuptools
from pathlib import Path

setuptools.setup(
    name="samatic",
    version="1.0.0",
    author="Sam",
    description="A fun console mood booster!",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(exclude=["tests", "data"]),
    python_requires=">=3.7",
)
