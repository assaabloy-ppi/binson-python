from setuptools import setup, find_packages

setup(name='binson_python',
      version='0.1',
      description='Binson implementation in python',
      url='http://github.com/sijohans',
      author='Simon Johansson',
      author_email='simon.johansson@assaabloy.com',
      license='MIT',
      packages=find_packages(exclude=('tests')),
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose'])