# enrich
Convenient GO enrichments from python. For use in `python` projects.

1. Builds the GO-ontology graph
2. Propagates GO-annotations up the graph
3. Performs enrichment test for all categories
4. Performs multiple testing correction
5. Allows for export to `graphviz` for visualization

## Installation

Download annotations from `geneontology.org`

```shell
mkdir db
wget http://purl.obolibrary.org/obo/go/go-basic.obo -O db/go-basic.obo
wget http://geneontology.org/gene-associations/gene_association.goa_ref_human.gz -O db/gene_association.goa_ref_human.gz
```

Clone the repository and add the path to you `$PYTHONPATH`. A package configuration will follow soon.

## Run GO enrichment

Construct the background and the query protein set

```python
from enrich import goa
background = goa.read('db/gene_association.goa_ref_human.gz')
query = set(background['db_object_id'].unique()[:20])
```

Build the ontology graph

```python
from enrich import obo
G = obo.graph('db/go-basic.obo')
```

Run the enrichment

```python
from enrich.enrichment import *
set_background(G, background)
pvalues = calculate_pvalues(G, query)
multiple_testing_correction(G, pvalues)
sig = filter_significant(G)
```

Export to `.dot` for visualization

```python
R = export_graphviz(G, sig, 'test.dot')
```

Generate `pdf` using graphviz

```shell
dot -Tpdf test.dot > test.pdf
```

# Licence

This work is licenced under the MIT licence

Contributions are welcome!
