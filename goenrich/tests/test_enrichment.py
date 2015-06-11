from unittest import TestCase

import goenrich

class TestGoenrich(TestCase):
    def test_entire_analysis(self):
        G = goenrich.obo.graph('db/go-basic.obo')
        for entry_id, category_id, background in [goenrich.read.goa('db/gene_association.goa_ref_human.gz'), goenrich.read.gene2go('db/gene2go.gz')]:
            query = set(background[entry_id].unique()[:20])
            goenrich.enrich.set_background(G, background, entry_id, category_id)
            pvalues = goenrich.enrich.calculate_pvalues(G, query)
            goenrich.enrich.multiple_testing_correction(G, pvalues)
            sig = goenrich.enrich.filter_significant(G)
            R = goenrich.export.to_graphviz(G, sig, '{}_test.dot'.format(entry_id))
