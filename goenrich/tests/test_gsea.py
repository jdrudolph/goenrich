from unittest import TestCase
import goenrich

class TestGoenrich(TestCase):

    def test_gsea(self):
        G = goenrich.obo.graph('db/go-basic.obo')
        gene2go = goenrich.read.gene2go('db/gene2go.gz')
        goenrich.enrich.set_background(G, gene2go, 'GeneID', 'GO_ID')
        
        MAPK_cascade = G.node['GO:0000165']['background']
        gene2go['MAPK_cascade'] = gene2go['GeneID'].isin(list(MAPK_cascade)[:-10])
        genes = gene2go.sort('MAPK_cascade', ascending=False)['GeneID'].unique()
