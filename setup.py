from setuptools import setup

def readme():
    try:
        from pypandoc import convert
        return convert('README.md', 'rst', format='markdown_github')
    except ImportError:
        import warnings
        warnings.warn('could not import pypandoc -- not converting README to rst', ImportWarning)
        with open('README.md') as f:
            return f.read()

setup(name='goenrich',
      version='1.0.0',
      description='GO enrichment with python -- pandas meets networkx',
      long_description=readme(),
      classifiers=[
          'Development Status :: 4 - Beta',
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
          'statsmodels',
          'networkx'],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)
