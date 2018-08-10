import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="concoursepy",
    version="0.0.2",
    author="Alex Arwine",
    author_email="arwineap@gmail.com",
    description="library to interface with concourse",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arwineap/concoursepy",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests'
    ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
