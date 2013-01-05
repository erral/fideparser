from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='fideparser',
      version=version,
      description="A package to export tournament info from FIDE site",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='fide rating export',
      author='Mikel Larreategi',
      author_email='larreategi@eibar.org',
      url='http://github.com/erral/fideparser',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'beautifulsoup4',
      ],
      entry_points={
        'console_scripts': [
              'export = fideparser.main:main',
        ]
      },
      )
