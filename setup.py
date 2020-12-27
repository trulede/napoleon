import os
from setuptools import setup, find_packages


def read(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as file:
        return file.read().strip()


setup(
    name="napoleon",
    version=os.getenv("VERSION", read("VERSION")),
    author="Timothy Rule",
    author_email="tim.rule.xing@gmail.com",
    license="MIT",
    description="Sphinx Napoleon Builder",
    url="https://github.com/trulede/napoleon.git",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "gitpython",
        "requests",
        "sphinx",
        "sphinx-rtd-theme",
    ],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "napoleon=napoleon.cli:main",
        ],
    },
)
