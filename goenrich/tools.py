"""
helper functions for `goenrich`
"""
import pandas as pd
import numpy as np

def generate_background(annotations, df, go_id, entry_id):
    """ generate the backgound from pandas datasets

    >>> O = ontology(...)
    >>> annotations = goenrich.read.gene2go(...)
    >>> background = generate_background(annotations, df, 'GO_ID', 'GeneID')
    >>> propagate(O, background, ...)

    :param annotations: pd.DataFrame containing the annotations
    :param df: pd.DataFrame containing the background genes
    :param go_id: GO id column name
    :param entry_id: Gene id column name
    :returns: dictionary with the background annotations
    """
    return {k : set(v) for k,v in
            pd.merge(annotations, df[[entry_id]]).groupby(go_id)[entry_id]}


def _ecdf(x):
    nobs = len(x)
    return np.arange(1,nobs+1)/float(nobs)

def fdrcorrection(pvals, alpha=0.05):
    """ benjamini hocheberg fdr correction. inspired by statsmodels """
    pvals = np.asarray(pvals)
    pvals_sortind = np.argsort(pvals)
    pvals_sorted = np.take(pvals, pvals_sortind)
    ecdffactor = _ecdf(pvals_sorted)
    reject = pvals_sorted <= ecdffactor*alpha
    if reject.any():
        rejectmax = max(np.nonzero(reject)[0])
        reject[:rejectmax] = True
    pvals_corrected_raw = pvals_sorted / ecdffactor
    pvals_corrected = np.minimum.accumulate(pvals_corrected_raw[::-1])[::-1]
    del pvals_corrected_raw
    pvals_corrected[pvals_corrected>1] = 1
    pvals_corrected_ = np.empty_like(pvals_corrected)
    pvals_corrected_[pvals_sortind] = pvals_corrected
    del pvals_corrected
    reject_ = np.empty_like(reject)
    reject_[pvals_sortind] = reject
    return reject_, pvals_corrected_
