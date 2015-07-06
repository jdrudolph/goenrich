import os
import pickle
import unittest
import goenrich
import networkx as nx

if os.path.isfile('.gene2go.pkl'):
    with open('.gene2go.pkl', 'rb') as f:
        G = pickle.load(f)
else:
    with open('.gene2go.pkl', 'wb') as f:
        O = goenrich.obo.graph('db/go-basic.obo', ontology_cache='.basic.pkl')
        gene2go = goenrich.read.gene2go('db/gene2go.gz')
        G = goenrich.enrich.set_background(O, gene2go, 'GeneID', 'GO_ID',
                background_name='gene2go')
        pickle.dump(G, f)

goslim = 'goslim_generic'

class TestGoslim(unittest.TestCase):
    def test_goslim_parsed(self):
        self.assertTrue('goslims' in G.graph)
        self.assertTrue(goslim in G.graph['goslims'])

    def test_goslim_set_in_at_least_one_node(self):
        for n, data in G.nodes(data=True):
            if goslim in data.get('subset', set()):
                return
        self.fail('goslim not found')

    def test_goslim_subset(self):
        S = goenrich.goslim.subset(G, goslim)
        # all nodes should have the correct goslim
        # there should be no orphans 
        for n, data in S.nodes(data=True):
            self.assertIn(goslim, data['subset'])
            self.assertGreater(S.degree(n), 0, n)  

if __name__ == '__main__':
    unittest.main()
