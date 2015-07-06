from unittest import TestCase

import goenrich

class TestRead(TestCase):
    def test_ontology(self):
        G = goenrich.obo.graph('db/go-basic.obo')
        self.assertTrue('goslim_generic' in G.graph['goslims'])

    def test_goa(self):
        background = goenrich.read.goa('db/gene_association.goa_ref_human.gz')

    def test_gene2go(self):
        background = goenrich.read.gene2go('db/gene2go.gz')
