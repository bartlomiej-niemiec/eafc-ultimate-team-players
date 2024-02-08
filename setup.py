from setuptools import setup, find_packages
from setuptools.command.install import install
import pathlib

here = pathlib.Path(__file__).parent.resolve()

VERSION = '0.0.1'
DESCRIPTION = 'FUT players scraper'
LONG_DESCRIPTION = (here / "README.md").read_text(encoding="utf-8")

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="fut-players",
    version=VERSION,
    author="Bartlomiej Niemiec",
    author_email="<bniemiec11@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url="https://github.com/bartlomiej-niemiec/fut-players",
    packages=find_packages(where="src"),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'tqdm'
    ],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'

    keywords=['python', 'eafc24', 'futwiz', 'fut', 'csv', 'multithreading'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3.9",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    package_dir={"": "src"},
)