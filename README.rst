goenrich
========

.. image:: https://badges.gitter.im/Join%20Chat.svg
    :target: https://gitter.im/jdrudolph/goenrich?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge
    :alt: gitter.im chat

.. image:: https://readthedocs.org/projects/goenrich/badge/?version=latest
    :alt: Documentation Status
    :scale: 100%
    :target: https://goenrich.readthedocs.org/en/latest 

Convenient GO enrichments from python. For use in ``python`` projects.

#. Builds the GO-ontology graph
#. Propagates GO-annotations up the graph
#. Subsetting using goslim
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
    # Entrez GeneID
    wget ftp://ftp.ncbi.nlm.nih.gov/gene/DATA/gene2go.gz -O db/gene2go.gz

Run GO enrichment
-----------------

.. code:: python

  import goenrich

  # build the ontology
  O = goenrich.obo.graph('db/go-basic.obo')

  # use all entrez geneid associations form gene2go as background
  # use goenrich.read.goa('db/gene_association.goa_ref_human.gz') for uniprot
  background = goenrich.read.gene2go('db/gene2go.gz')
  G = goenrich.enrich.set_background(O, background, 'GeneID', 'GO_ID')

  # extract some list of entries as example query
  query = set(background['GeneID'].unique()[:20])

  # for additional export to graphviz just specify the gvfile argument
  # the show argument keeps the graph reasonably small
  result = goenrich.enrich.analyze(G, query, gvfile='example.dot', show='top20')

.. raw:: html

  <table border="1" class="dataframe">
    <thead>
      <tr style="text-align: right;">
        <th></th>
        <th>name</th>
        <th>x</th>
        <th>p</th>
        <th>q</th>
        <th>namespace</th>
      </tr>
      <tr>
        <th>term</th>
        <th></th>
        <th></th>
        <th></th>
        <th></th>
        <th></th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <th>GO:0005215</th>
        <td>transporter activity</td>
        <td>2</td>
        <td>0.015062</td>
        <td>0.017070</td>
        <td>molecular_function</td>
      </tr>
      <tr>
        <th>GO:0009719</th>
        <td>response to endogenous stimulus</td>
        <td>4</td>
        <td>0.000056</td>
        <td>0.000181</td>
        <td>biological_process</td>
      </tr>
      <tr>
        <th>GO:1901699</th>
        <td>cellular response to nitrogen compound</td>
        <td>2</td>
        <td>0.000631</td>
        <td>0.001227</td>
        <td>biological_process</td>
      </tr>
      <tr>
        <th>GO:0060089</th>
        <td>molecular transducer activity</td>
        <td>2</td>
        <td>0.022831</td>
        <td>0.023523</td>
        <td>molecular_function</td>
      </tr>
      <tr>
        <th>GO:0019725</th>
        <td>cellular homeostasis</td>
        <td>2</td>
        <td>0.001838</td>
        <td>0.002907</td>
        <td>biological_process</td>
      </tr>
    </tbody>
  </table>

Generate ``png`` image using graphviz

.. code:: shell

    dot -Tpng example.dot > example.png

.. image:: https://cloud.githubusercontent.com/assets/2606663/8525018/cad3a288-23fe-11e5-813c-bd205a47eed8.png

GO-slim
---------

.. code:: python

  # dowload goslim from ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/goslim/goslim_goa.obo
  goa_slim = goenrich.goslim.read('db/goslim_goa.obo')
  goenrich.goslim.add(G, 'goslim_goa', (n for n in goa_slim if n in G))
  S = goenrich.goslim.subset(G, 'goslim_goa')
  result_slim = goenrich.enrich.analyze(S, query, gvfile='example_slim.dot', show='top20')

Parameters
~~~~~~~~~~

Parameters can all be passed to ``enrich.analyze`` as shown below

.. code:: python

    go_options = {
            'multiple-testing-correction' : 'bonferroni',
            'alpha' : 0.05,
            'node_filter' : lambda x : x.get('significant', False)
    }
    goenrich.enrich.analyze(G, query, **go_options)

    # export results to graphviz
    goenrich.enrich.analyze(G, query, gvfile='example.dot', **go_options)

Here is an overview over the available parmeters

::

    read.*:
      experimental = True # don't consider inferred annotations

    enrich.analyze:
      node_filter = lambda node : 'p' in node
      show = 'top20' # works for any 'topNUM'

    enrich.calculate_pvalues:
      min_hit_size = 2
      min_category_size = 3
      max_category_size = 500
      max_category_depth = 5

    enrich.multiple_testing_correction:
      alpha = 0.05
      method = 'benjamin-hochberg' # also supported : 'bonferroni'

    export.to_frame:
      node_filter = lambda node: True

    export.to_graphviz:
      graph_label = None # if None it is replaced by multiple testing info

Licence
=======

This work is licenced under the MIT licence

Contributions are welcome!

Building the documentation
==========================

sphinx-apidoc -f -o docs goenrich goenrich/tests

