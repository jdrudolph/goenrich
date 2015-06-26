import pandas as pd
import numpy as np
import goenrich

G = goenrich.obo.graph('db/go-basic.obo')
goa = goenrich.read.goa('db/gene_association.goa_ref_human.gz')
symbol = 'db_object_symbol'
reference = pd.read_table('db/referenceGenes.txt', names=[symbol])

background = pd.merge(goa, reference)
goenrich.enrich.set_background(G, background, symbol, 'go_id')

interesting = pd.read_table('db/interestingGenes.txt', names=[symbol])
reference['interesting'] = reference[symbol].isin(interesting[symbol])
genes = reference.sort('interesting', ascending=False)[symbol].values.astype(str)
ontology = G

min_category_size = 3
permutations = 10

