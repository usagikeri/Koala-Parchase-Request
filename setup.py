from setuptools import setup, find_packages

setup(name='koala',
      version='0.0.1',
      description='koala commandline-tools',
      author='usagikeri',
      packages=find_packages(),
      py_modules = ['Koala_tools', 'koala_info', 'get_info', 'koala_search', 'main'],
      entry_points="""
      [console_scripts]
      koala = main:main
      """)
