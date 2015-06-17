from setuptools import setup

def readme():
    try:
        from pypandoc import convert
        _readme = convert('README.md', 'rst', format='markdown_github')
        lines = []
        in_table = 0
        for line in _readme.splitlines():
            if line == 'The resulting table is:':
                in_table = 3
            elif line == '':
                in_table = in_table - 1
            if in_table > 0:
                continue
            else:
                lines.append(line)
        return '\n'.join(lines)
    except ImportError:
        import warnings
        warnings.warn('could not import pypandoc -- not converting README to rst', ImportWarning)
        with open('README.md') as f:
            return f.read()

setup(name='goenrich',
      version='1.1.1',
      description='GO enrichment with python -- pandas meets networkx',
      long_description=readme(),
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.4',
          'Topic :: Scientific/Engineering :: Bio-Informatics',
          'Topic :: Software Development :: Libraries'],
      keywords= ['GO', 'Gene Ontology', 'Biology', 'Enrichment',
          'Bioinformatics', 'Computational Biology',
          'library',
          'visualization', 'graphviz', 'pandas'],
      url='https://github.com/jdrudolph/goenrich',
      download_url='https://github.com/jdrudolph/goenrich/tarball/v1.0',
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
