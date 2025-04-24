from setuptools import setup, find_packages
from pkg_resources import parse_requirements
import pathlib

def load_requirements(path):
    """Parse requirements.txt using pkg_resources.parse_requirements()"""
    path = pathlib.Path(path)
    with open(path) as f:
        lines = f.readlines()
    reqs = []
    for req in parse_requirements(lines):
        # Each req is a Requirement object, convert back to PEP 508 string
        reqs.append(str(req))
    return reqs

setup(
    name="my_project_require",
    version="0.1.0",
    description="Example using pkg_resources.parse_requirements",
    long_description=pathlib.Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your@email.com",
    url="https://example.com/my_project",
    packages=find_packages(),
    include_package_data=True,
    install_requires='requests',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.7",
)

