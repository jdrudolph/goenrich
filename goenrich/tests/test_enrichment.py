import unittest
import os
import pickle
import subprocess
import goenrich

cache = '.test_cache.pkl'
if os.path.isfile(cache):
    with open(cache, 'rb') as f:
        O, G_gene2go, G_goa, goa, gene2go = pickle.load(f)
else:
    with open(cache, 'wb') as f:
        O = goenrich.obo.graph('db/go-basic.obo', ontology_cache='.basic.pkl')
        goa = [goenrich.read.goa('db/gene_association.goa_ref_human.gz'), 'db_object_id', 'go_id']
        gene2go = [goenrich.read.gene2go('db/gene2go.gz'), 'GeneID', 'GO_ID']
        G_gene2go = goenrich.enrich.set_background(O, *gene2go)
        G_goa = goenrich.enrich.set_background(O, *goa)
        pickle.dump((O, G_gene2go, G_goa, goa, gene2go), f)

query = set(goa[0]['db_object_id'].unique()[:20])

def backgrounds_equal(G, H):
    """ test if node attributes of all nodes are identical """
    return (all(G.node[g].get('background', set()) == H.node.get(g, {}).get('background', set()) for g in G)
            and all(H.node[h].get('background', set()) == G.node.get(h, {}).get('background', set()) for h in H))

class TestGoenrich(unittest.TestCase):

    def test_set_background_inplace(self):
        H = O.copy()
        goenrich.enrich.set_background(H, *goa, inplace=True)
        self.assertTrue(backgrounds_equal(H, G_goa))
         
        goenrich.enrich.set_background(H, *gene2go, inplace=True)
        self.assertTrue(backgrounds_equal(H, G_gene2go))
        
    def test_calculate_pvalues_inplace(self):
        H = G_goa.copy()

        q1 = query
        q2 = set(goa[0]['db_object_id'].unique()[21:40])
         
        df1 = goenrich.enrich.analyze(H, q1)
        df2 = goenrich.enrich.analyze(H, q2)

        df11 = goenrich.enrich.analyze(H, q1)
        from pandas.util.testing import assert_frame_equal
        with self.assertRaises(AssertionError):
            assert_frame_equal(df1, df2) # different query
        assert_frame_equal(df1, df11) # same query

    def test_analysis_and_export(self):
        H, pvalues = goenrich.enrich.calculate_pvalues(G_goa, query)
        I = goenrich.enrich.multiple_testing_correction(H, pvalues)
        df = goenrich.export.to_frame(I, node_filter=lambda node : 'q' in node)
        sig = df[df['significant']].sort('q').head(20).index
        
        try:
            import pygraphviz
            # gvfile is file
            with open('test.dot', 'w') as gvfile:
                goenrich.export.to_graphviz(I, sig, gvfile)
            subprocess.check_call(['dot', '-Tpng', 'test.dot', '-o', 'test.png'])
            subprocess.check_call(['rm', 'test.dot', 'test.png'])
           
            # gvfile is string
            gvfile = 'test.dot'
            goenrich.export.to_graphviz(I, sig, gvfile)
            subprocess.check_call(['dot', '-Tpng', 'test.dot', '-o', 'test.png'])
            subprocess.check_call(['rm', 'test.dot', 'test.png'])
        except ImportError:
            print('pygraphviz could not be imported')

if __name__ == '__main__':
    unittest.main()
