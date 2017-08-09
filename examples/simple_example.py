"""
README.md example
"""

import goenrich

# build the ontology
O = goenrich.obo.ontology('db/go-basic.obo')

# use all entrez geneid associations form gene2go as background
# use goenrich.read.goa('db/gene_association.goa_human.gaf.gz') for uniprot
gene2go = goenrich.read.gene2go('db/gene2go.gz')
values = {k: set(v) for k,v in gene2go.groupby('GO_ID')['GeneID']}

# propagate the background through the ontology
background_attribute = 'gene2go'
goenrich.enrich.propagate(O, values, background_attribute)

# extract some list of entries as example query
query = gene2go['GeneID'].unique()[:20]

# for additional export to graphviz just specify the gvfile argument
# the show argument keeps the graph reasonably small
df = goenrich.enrich.analyze(O, query, background_attribute, gvfile='example.dot')

# generate html
df.dropna().head().to_html('example.html')

# call to graphviz
import subprocess
subprocess.check_call(['dot', '-Tpng', 'example.dot', '-o', 'example.png'])
