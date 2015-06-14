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

# use all associations as background
entry_id, category_id, background = goenrich.read.goa('db/gene_association.goa_ref_human.gz')
# use goenrich.read.gene2go('db/gene2go.gz') for entrez geneid
# extract some list of entries as query
query = set(background[entry_id].unique()[:20])

# set background
goenrich.enrich.set_background(G, background)

# run enrichment analysis, correct for multiple testing
pvalues = goenrich.enrich.calculate_pvalues(G, query, entry_id, category_id)
goenrich.enrich.multiple_testing_correction(G, pvalues)

# export to pandas or graphviz
df = goenrich.export.to_frame(G)
sig = goenrich.enrich.filter_significant(G)
R = goenrich.export.to_graphviz(G, sig, 'test.dot')
```

Generate `png` image using graphviz

```shell
dot -Tpng test.dot > test.png
```

![Example output](https://cloud.githubusercontent.com/assets/2606663/8107738/435fba70-1054-11e5-9ef5-252bbcec65e8.png)

### Parameters

Some parameters to consider for analysis
```
enrich.calculate_pvalues:
  min_category_size = 2

enrich.multiple_testing_correction:
  alpha = 0.05
  method = ['benjamin-hochberg', 'bonferroni']
```

# Licence

This work is licenced under the MIT licence

Contributions are welcome!
