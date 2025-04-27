from setuptools import setup, find_packages

setup(
    name="algoinfinite",
    version="0.1.1",
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
)

