from setuptools import find_packages
from setuptools import setup

import os


version = '1.0.2'

TEST_REQUIRES = ["responses", "mock"]

setup(
    name="fideparser",
    version=version,
    description="A package to export tournament info from FIDE site",
    long_description=open("README.rst").read()
    + "\n"
    + open(os.path.join("docs", "HISTORY.txt")).read(),
    classifiers=[],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords="fide rating export",
    author="Mikel Larreategi",
    author_email="larreategi@eibar.org",
    url="https://github.com/erral/fideparser",
    license="GPL",
    packages=find_packages(exclude=["ez_setup", "examples", "tests"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
        "beautifulsoup4",
        "requests",
        "unicodecsv",
    ],
    extras_require={"test": TEST_REQUIRES},
    entry_points={
        "console_scripts": [
            "export_fide_tournaments = fideparser.main:main",
            "merge_csv_files = fideparser.mergecsv:main",
        ]
    },
)
