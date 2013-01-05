from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='fideparser',
      version=version,
      description="A package to export tournament info from FIDE site",
      long_description="""\
""",
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
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
