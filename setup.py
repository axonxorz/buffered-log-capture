from setuptools import setup, find_packages


setup(name='buffered_log_capture',
      version='0.0.1',
      description=u"Buffered logging output capture",
      long_description=None,
      classifiers=[],
      keywords='',
      author=u"Brendan Zerr",
      author_email='bzerr@brainwire.ca',
      url='https://github.com/axonxorz/buffered_log_capture',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[],
      extras_require={},
      entry_points=None
      )
