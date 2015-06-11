from unittest import TestCase

import goenrich

class TestRead(TestCase):
    def test_goa(self):
        background = goenrich.read.goa('db/gene_association.goa_ref_human.gz')

    def test_gene2go(self):
        background = goenrich.read.gene2go('db/gene2go.gz')
