from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    author="James",
    description="A tool to parse a fixed width file",
    entry_points={
        "console_scripts": [
            "parse=fwf_parser.cli:parse"
        ]
    },
    install_requires=requirements,
    name="parse",
    packages=find_packages(exclude=["tests", "scripts", "sample_data"]),
    url="https://github.com/jamessuperlee/fixed_width_parser",
    version="0.0.1"
)
