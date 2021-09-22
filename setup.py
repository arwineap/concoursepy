import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


def read_requirements(filename):
    with open(filename) as fh:
        lines = fh.readlines()
    # remove comments
    lines = [line.split('#')[0] for line in lines]
    # remove trailing spaces
    lines = [line.strip() for line in lines]
    # remove empty lines
    lines = [line for line in lines if line]
    return lines


setuptools.setup(
    name="concoursepy",
    version="0.0.30",
    author="Alex Arwine",
    author_email="arwineap@gmail.com",
    description="library to interface with concourse",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arwineap/concoursepy",
    packages=setuptools.find_packages(),
    install_requires=read_requirements('requirements.txt'),
    tests_require=read_requirements('test-requirements.txt'),
    include_package_data=True,
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
