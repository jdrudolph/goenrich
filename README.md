# goenrich
Convenient GO enrichments from python. For use in `python` projects.

1. Builds the GO-ontology graph
2. Propagates GO-annotations up the graph
3. Performs enrichment test for all categories
4. Performs multiple testing correction
5. Allows for export to `graphviz` for visualization

## Installation

Install package from pypi and download annotations from `geneontology.org`

```shell
pip install goenrich
mkdir db
wget http://purl.obolibrary.org/obo/go/go-basic.obo -O db/go-basic.obo
wget http://geneontology.org/gene-associations/gene_association.goa_ref_human.gz -O db/gene_association.goa_ref_human.gz
```

## Run GO enrichment

```python
import goenrich

# use all associations as background
background = goenrich.goa.read('db/gene_association.goa_ref_human.gz')
# extract some list of UniprotACC as query
query = set(background['db_object_id'].unique()[:20])

# build the ontology and apply background
G = goenrich.obo.graph('db/go-basic.obo')
goenrich.enrich.set_background(G, background)

# run enrichment analysis, correct for multiple testing
# and export to graphviz
pvalues = goenrich.enrich.calculate_pvalues(G, query)
goenrich.enrich.multiple_testing_correction(G, pvalues)
sig = goenrich.enrich.filter_significant(G)
R = goenrich.export.to_graphviz(G, sig, 'test.dot')
```

Generate `pdf` using graphviz

```shell
dot -Tpdf test.dot > test.pdf
```

![Example output](https://cloud.githubusercontent.com/assets/2606663/8107738/435fba70-1054-11e5-9ef5-252bbcec65e8.png)

### Parameters

```
enrich.calculate_pvalues: min_category_size = 2
```

# Licence

This work is licenced under the MIT licence

Contributions are welcome!
