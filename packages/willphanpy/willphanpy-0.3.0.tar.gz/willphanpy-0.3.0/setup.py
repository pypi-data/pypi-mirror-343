from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name = 'willphanpy',
    version = '0.3.0',
    packages=find_packages(),
    install_requires=[
        "numpy",
        "matplotlib",
    ],
    long_description=description,
    long_description_content_type = "text/markdown"
)