from unittest import TestCase

import goenrich

G = goenrich.obo.graph('db/go-basic.obo')
goa = goenrich.read.goa('db/gene_association.goa_ref_human.gz')
gene2go = goenrich.read.gene2go('db/gene2go.gz')

class TestGoenrich(TestCase):
    def test_entire_analysis(self):
        for entry_id, category_id, background in [goa, gene2go]:
            query = set(background[entry_id].unique()[:20])
            goenrich.enrich.set_background(G, background, entry_id, category_id)
            pvalues = goenrich.enrich.calculate_pvalues(G, query)
            goenrich.enrich.multiple_testing_correction(G, pvalues)
            df = goenrich.export.to_frame(G)
            sig = goenrich.enrich.filter_significant(G)
            R = goenrich.export.to_graphviz(G, sig, '{}_test.dot'.format(entry_id))
