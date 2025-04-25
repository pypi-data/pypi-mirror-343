from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="package_shakarpg",
    version="0.0.1",
    author="shakarpg",
    author_email="rafinharpg@gmail.com",
    description="projeto pypi",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shakarpg/simple-package-template.git" ,
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)
