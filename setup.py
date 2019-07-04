from setuptools import setup, find_packages


######################################################################################
with open("README.md", "r") as readme_file:
    readme = readme_file.read()


######################################################################################
setup(
    name="pycvss",
    version="0.0.1",
    author="Holden Babineaux",
    author_email="holden.bab@outlook.com",
    description="A python module for the CVSS architecture designed for research and service provision.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/HoldenB/pycvss",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7"
    ],
)
