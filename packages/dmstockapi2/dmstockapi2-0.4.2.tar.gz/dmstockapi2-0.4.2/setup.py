from setuptools import setup, find_packages

setup(
    name="dmstockapi2",
    version="0.4.2",
    url="",
    license="Apache-2.0",
    author="James Liu",
    author_email="",
    description="",
    packages=find_packages(exclude=("tests")),
    install_requires=["pandas >= 2.2.2", "requests >= 2.22.0"],
)
