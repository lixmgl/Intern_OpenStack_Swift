from setuptools import setup, find_packages
import sys, os

version = '0.0.1'

setup(name='swiftstats',
      version=version,
      description="Swift statistic data collection and feeds to statsd",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='swiftstats',
      author='Autumn Wang',
      author_email='autumn@cisco.com',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests', 'utils']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      scripts=['bin/swiftstats-server', 'bin/swiftstats'],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
