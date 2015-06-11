from unittest import TestCase

import goenrich

class TestGoenrich(TestCase):
    def test_if_runs_through(self):
        background = goenrich.goa.read('db/gene_association.goa_ref_human.gz')
        G = goenrich.obo.graph('db/go-basic.obo')
        query = set(background['db_object_id'].unique()[:20])
        goenrich.enrich.set_background(G, background)
        pvalues = goenrich.enrich.calculate_pvalues(G, query)
        goenrich.enrich.multiple_testing_correction(G, pvalues)
        sig = goenrich.enrich.filter_significant(G)
        R = goenrich.export.to_graphviz(G, sig, 'test.dot')
