import pandas as pd
GENE_ASSOCIATION_COLUMNS = ('db', 'db_object_id', 'db_object_symbol',
                            'qualifier', 'go_id', 'db_reference',
                            'evidence_code', 'with_from', 'aspect',
                            'db_object_name', 'db_object_synonym',
                            'db_object_type', 'taxon', 'date', 'assigned_by',
                            'annotation_extension', 'gene_product_form_id')
EXPERIMENTAL_EVIDENCE = ('EXP', 'IDA', 'IPI', 'IMP', 'IGI', 'IEP')
def goa(filename, experimental=True, **kwds):
    """ read go-annotation file
    :returns:
        entry_id: protein or gene identifier column
        category_id: GO term column
        background: background annotation set
    """
    defaults = {'comment' : '!',
            'compression' : 'gzip',
            'names': GENE_ASSOCIATION_COLUMNS}

    if experimental and 'usecols' in kwds:
        kwds['usecols'] += ('evidence_code', )

    defaults.update(kwds)
    result = pd.read_table(filename, **defaults)

    if experimental:
        retain_mask = result.evidence_code.isin(EXPERIMENTAL_EVIDENCE)
        result.drop(result.index[~retain_mask], inplace=True)

    return 'db_object_id', 'go_id', result


GENE2GO_COLUMNS = ('tax_id', 'GeneID', 'GO_ID', 'Evidence', 'Qualifier', 'GO_term', 'PubMed', 'Category')
def gene2go(filename, experimental=True, tax_id=9606, **kwds):
    """ read go-annotation file
    :returns:
        entry_id: protein or gene identifier column
        category_id: GO term column
        background: background annotation set
    """
    defaults = {'compression' : 'gzip',
            'comment' : '#',
            'names' : GENE2GO_COLUMNS }
    defaults.update(kwds)
    result = pd.read_table(filename, **defaults)
    
    retain_mask = result.tax_id == tax_id
    result.drop(result.index[~retain_mask], inplace=True)

    if experimental:
        retain_mask = result.Evidence.isin(EXPERIMENTAL_EVIDENCE)
        result.drop(result.index[~retain_mask], inplace=True)

    return 'GeneID', 'GO_ID', result

