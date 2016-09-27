goenrich
========

.. image:: https://badges.gitter.im/Join%20Chat.svg
    :target: https://gitter.im/jdrudolph/goenrich?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge

.. image:: https://readthedocs.org/projects/goenrich/badge/?version=latest
    :scale: 100%
    :target: https://goenrich.readthedocs.org/en/latest 

.. image:: https://travis-ci.org/jdrudolph/goenrich.svg?branch=master
    :target: https://travis-ci.org/jdrudolph/goenrich

Convenient GO enrichments from python. For use in ``python`` projects.

#. Builds the GO-ontology graph
#. Propagates GO-annotations up the graph
#. Performs enrichment test for all categories
#. Performs multiple testing correction
#. Allows for export to ``pandas`` for processing and ``graphviz`` for
   visualization

Installation
------------

| Install package from pypi and download ontology
| and needed annotations.

.. code:: shell

    pip install goenrich
    mkdir db
    # Ontology
    wget http://purl.obolibrary.org/obo/go/go-basic.obo -O db/go-basic.obo
    # UniprotACC
    wget http://geneontology.org/gene-associations/gene_association.goa_ref_human.gz -O db/gene_association.goa_ref_human.gz
    # Yeast SGD
    wget http://downloads.yeastgenome.org/curation/literature/gene_association.sgd.gz -O db/gene_association.sgd.gz
    # Entrez GeneID
    wget ftp://ftp.ncbi.nlm.nih.gov/gene/DATA/gene2go.gz -O db/gene2go.gz

Run GO enrichment
-----------------

.. code:: python

  import goenrich

  # build the ontology
  O = goenrich.obo.ontology('db/go-basic.obo')

  # use all entrez geneid associations form gene2go as background
  # use annot = goenrich.read.goa('db/gene_association.goa_ref_human.gz') for uniprot
  # use annot = goenrich.read.sgd('db/gene_association.sgd.gz') for yeast
  gene2go = goenrich.read.gene2go('db/gene2go.gz')
  # use values = {k: set(v) for k,v in annot.groupby('go_id')['db_object_symbol']} for uniprot/yeast
  values = {k: set(v) for k,v in gene2go.groupby('GO_ID')['GeneID']}

  # propagate the background through the ontology
  background_attribute = 'gene2go'
  goenrich.enrich.propagate(O, values, background_attribute)

  # extract some list of entries as example query
  # use query = annot['db_object_symbol'].unique()[:20]
  query = gene2go['GeneID'].unique()[:20]

  # for additional export to graphviz just specify the gvfile argument
  # the show argument keeps the graph reasonably small
  df = goenrich.enrich.analyze(O, query, background_attribute, gvfile='test.dot')

  # generate html
  df.dropna().head().to_html('example.html')

  # call to graphviz
  import subprocess
  subprocess.check_call(['dot', '-Tpng', 'test.dot', '-o', 'test.png'])

.. raw:: html

  <table border="1" class="dataframe">
    <thead>
      <tr style="text-align: right;">
        <th></th>
        <th>name</th>
        <th>namespace</th>
        <th>p</th>
        <th>q</th>
        <th>rejected</th>
        <th>term</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <th>1245</th>
        <td>response to organic cyclic compound</td>
        <td>biological_process</td>
        <td>2.856257e-06</td>
        <td>6.732606e-06</td>
        <td>1</td>
        <td>GO:0014070</td>
      </tr>
      <tr>
        <th>1668</th>
        <td>ATP binding</td>
        <td>molecular_function</td>
        <td>8.821334e-09</td>
        <td>3.325412e-07</td>
        <td>1</td>
        <td>GO:0005524</td>
      </tr>
      <tr>
        <th>1988</th>
        <td>phosphorylation</td>
        <td>biological_process</td>
        <td>1.101491e-03</td>
        <td>1.118437e-03</td>
        <td>1</td>
        <td>GO:0016310</td>
      </tr>
      <tr>
        <th>3319</th>
        <td>cellular response to organonitrogen compound</td>
        <td>biological_process</td>
        <td>2.639774e-05</td>
        <td>5.084590e-05</td>
        <td>1</td>
        <td>GO:0071417</td>
      </tr>
      <tr>
        <th>3422</th>
        <td>metal ion binding</td>
        <td>molecular_function</td>
        <td>1.719726e-05</td>
        <td>3.439452e-05</td>
        <td>1</td>
        <td>GO:0046872</td>
      </tr>
    </tbody>
  </table>

Generate ``png`` image using graphviz:

.. code:: shell

    dot -Tpng example.dot > example.png

or directly from python:

.. code:: python
  
  import subprocess
  subprocess.check_call(['dot', '-Tpng', 'example.dot', '-o', 'example.png'])

.. image:: https://cloud.githubusercontent.com/assets/2606663/8525018/cad3a288-23fe-11e5-813c-bd205a47eed8.png

Check the documentation for all available parameters

Licence
=======

This work is licenced under the MIT licence

Contributions are welcome!

Building the documentation
==========================

.. code:: shell

  sphinx-apidoc -f -o docs goenrich goenrich/tests

