from unittest import TestCase
import subprocess
import goenrich

G = goenrich.obo.graph('db/go-basic.obo')
goa = [goenrich.read.goa('db/gene_association.goa_ref_human.gz'), 'db_object_id', 'go_id']
gene2go = [goenrich.read.gene2go('db/gene2go.gz'), 'GeneID', 'GO_ID']

def graphs_equal(G, H):
    """ test if node attributes of all nodes are identical """
    return (all(G.node[g] == H.node.get(g, {}) for g in G)
            and all(H.node[h] == G.node.get(h, {}) for h in H))

class TestGoenrich(TestCase):

    def test_setting_different_backgrounds_do_not_interfere(self):
        G = goenrich.obo.graph('db/go-basic.obo')
        G1 = G.copy()
        goenrich.enrich.set_background(G1, *goa)
        G2 = G.copy()
        goenrich.enrich.set_background(G2, *gene2go)

        goenrich.enrich.set_background(G, *goa)
        assert graphs_equal(G, G1)

        goenrich.enrich.set_background(G, *gene2go)
        assert graphs_equal(G, G2)
        
    def test_multiple_queries_do_not_interfere(self):
        G = goenrich.obo.graph('db/go-basic.obo')
        background, entry_id, category_id = goa
        goenrich.enrich.set_background(G, *goa)

        q1 = set(background[entry_id].unique()[:20])
        q2 = set(background[entry_id].unique()[21:40])
         
        df1 = goenrich.enrich.analyze(G, q1)
        df2 = goenrich.enrich.analyze(G, q2)

        df11 = goenrich.enrich.analyze(G, q1)
        from pandas.util.testing import assert_frame_equal
        try:
            assert_frame_equal(df1, df2) # different query
            assert False
        except AssertionError:
            assert True
        assert_frame_equal(df1, df11) # same query

    def test_analysis_and_export(self):
        G = goenrich.obo.graph('db/go-basic.obo')
        background, entry_id, category_id = goa
        goenrich.enrich.set_background(G, *goa)
        query = set(background[entry_id].unique()[:20])
        df = goenrich.enrich.analyze(G, query)
        sig = df[df['significant']].index
        
        # gvfile is file
        with open('test.dot', 'w') as gvfile:
            goenrich.export.to_graphviz(G, sig, gvfile)
        subprocess.check_call(['dot', '-Tpng', 'test.dot', '-o', 'test.png'])
        subprocess.check_call(['rm', 'test.dot', 'test.png'])
       
        # gvfile is string
        gvfile = 'test.dot'
        goenrich.export.to_graphviz(G, sig, gvfile)
        subprocess.check_call(['dot', '-Tpng', 'test.dot', '-o', 'test.png'])
        subprocess.check_call(['rm', 'test.dot', 'test.png'])

