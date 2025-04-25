import setuptools

with open("../../README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="oxford_stats_lib",
    version="1.1.0",
    author="Geza Kerecsenyi",
    author_email="geza@kerecs.com",
    description="A library for wrangling data for University of Oxford Intro to Probability Theory and Statistics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)