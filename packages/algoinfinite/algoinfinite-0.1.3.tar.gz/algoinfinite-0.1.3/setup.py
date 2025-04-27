from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="algoinfinite",
    version="0.1.3",
    author="Madan Mohan Behera",
    author_email="madanmohan14072002@gmail.com",
    description="A collection of algorithms and data structures in Python.",
    packages=find_packages(),
    install_requires=[
        # Add any dependencies your package requires here
    ],
    entry_points={
        "console_scripts":[
            "madan-hello = algoinfinite:hello",
        ],
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
)

