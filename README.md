# goenrich
Convenient GO enrichments from python. For use in `python` projects.

1. Builds the GO-ontology graph
2. Propagates GO-annotations up the graph
3. Performs enrichment test for all categories
4. Performs multiple testing correction
5. Allows for export to `pandas` for processing and `graphviz` for visualization

Supported ids: `Uniport ACC`, `Entrez GeneID`

## Installation

Install package from pypi and download ontology
and needed annotations.

```shell
pip install goenrich
mkdir db
# Ontology
wget http://purl.obolibrary.org/obo/go/go-basic.obo -O db/go-basic.obo
# UniprotACC
wget http://geneontology.org/gene-associations/gene_association.goa_ref_human.gz -O db/gene_association.goa_ref_human.gz
# Entrez GeneID
wget ftp://ftp.ncbi.nlm.nih.gov/gene/DATA/gene2go.gz -O db/gene2go.gz
```

## Run GO enrichment

```python
import goenrich

# build the ontology
G = goenrich.obo.graph('db/go-basic.obo')

# use all entrez geneid associations form gene2go as background
# use goenrich.read.goa('db/gene_association.goa_ref_human.gz') for uniprot
background = goenrich.read.gene2go('db/gene2go.gz')
goenrich.enrich.set_background(G, background, 'GeneID', 'GO_ID')

# extract some list of entries as example query
query = set(background['GeneID'].unique()[:20])

# run analysis and obtain results
result = goenrich.enrich.analyze(G, query)

# for additional export to graphviz just specify the gvfile argument
# the show argument keeps the graph reasonably small
result = goenrich.enrich.analyze(G, query, gvfile='example.dot', show='top20')
```
The resulting table is:

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
      <th>GO:0044877</th>
      <td>macromolecular complex binding</td>
      <td>2</td>
      <td>3.422658e-02</td>
      <td>0.034227</td>
      <td>molecular_function</td>
    </tr>
    <tr>
      <th>GO:0000149</th>
      <td>SNARE binding</td>
      <td>2</td>
      <td>1.041071e-05</td>
      <td>0.000092</td>
      <td>molecular_function</td>
    </tr>
    <tr>
      <th>GO:1901700</th>
      <td>response to oxygen-containing compound</td>
      <td>2</td>
      <td>1.088637e-02</td>
      <td>0.014640</td>
      <td>biological_process</td>
    </tr>
    <tr>
      <th>GO:0050801</th>
      <td>ion homeostasis</td>
      <td>2</td>
      <td>1.653091e-03</td>
      <td>0.003393</td>
      <td>biological_process</td>
    </tr>
    <tr>
      <th>GO:0051353</th>
      <td>positive regulation of oxidoreductase activity</td>
      <td>2</td>
      <td>2.439696e-07</td>
      <td>0.000010</td>
      <td>biological_process</td>
    </tr>
  </tbody>
</table>

Generate `png` image using graphviz

```shell
dot -Tpng example.dot > example.png
```

![example](https://cloud.githubusercontent.com/assets/2606663/8212312/a851ba68-1523-11e5-9a6b-d4eaf25fb676.png)

### Parameters

Parameters can all be passed to `enrich.analyze` as shown below
```python
go_options = {
        'multiple-testing-correction' : 'bonferroni',
        'alpha' : 0.05,
        'node_filter' : lambda x : x.get('significant', False)
}
goenrich.enrich.analyze(G, query, **go_options)

# export results to graphviz
goenrich.enrich.analyze(G, query, gvfile='example.dot', **go_options)
```

Here is an overview over the available parmeters
```
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
```

# Licence

This work is licenced under the MIT licence

Contributions are welcome!
