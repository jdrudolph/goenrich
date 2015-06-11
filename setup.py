from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='goenrich',
      version='0.2.1',
      description='GO enrichment with python -- pandas meets networkx',
      long_description=readme(),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.4',
          'Topic :: Scientific/Engineering :: Bio-Informatics',
          'Topic :: Software Development :: Libraries'],
      url='http://github.com/jdrudolph/goenrich',
      author='Jan Daniel Rudolph',
      author_email='jan.daniel.rudolph@gmail.com',
      license='MIT',
      packages=['goenrich'],
      install_requires=[
          'numpy',
          'pandas',
          'scipy',
          'networkx'],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)
