from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

setup(
    name="ffmpeg-py",
    version="0.0.1",
    author="Holden Babineaux",
    author_email="holden.bab@outlook.com",
    description="A project for FFMPEG benchmarking and research.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/HoldenB/ffmpeg-py",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7"
    ],
)
