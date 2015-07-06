"""
README.md example
"""

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

# generate html
result[['name', 'x', 'p', 'q', 'namespace']].head().to_html('example.html')

# call to graphviz
import subprocess
subprocess.call(['dot', '-Tpng', 'example.dot', '-o', 'example.png'])


# goslim example
# dowload goslim from ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/goslim/goslim_goa.obo
goa_slim = goenrich.goslim.read('db/goslim_goa.obo')
goenrich.goslim.add(G, 'goslim_goa', (n for n in goa_slim if n in G))
S = goenrich.goslim.subset(G, 'goslim_goa')
result_slim = goenrich.enrich.analyze(S, query, gvfile='example_slim.dot', show='top20')

# generate html
result_slim[['name', 'x', 'p', 'q', 'namespace']].head().to_html('example_slim.html')

# call to graphviz
subprocess.call(['dot', '-Tpng', 'example_slim.dot', '-o', 'example_slim.png'])
