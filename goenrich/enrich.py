import networkx as nx
import numpy as np
from scipy.stats import hypergeom
from statsmodels.stats.multitest import fdrcorrection

def set_background(G, df, entry_id, category_id):
    """ Propagate background set through the ontolgy tree
    obtain parameters from goenrich.read
    >>> entry_id, category_id, background = goenrich.read.goa('...')

    :param entry_id: protein or gene identifier column
    :param category_id: GO term column
    """
    M = len(df[entry_id].unique()) # total number of objects
    for n in G: # clean background attribute for changing backgrounds
        node = G.node[n]
        node['background'] = set([])
        node['M'] = M

    grouped = df.groupby(category_id)[entry_id]
    for term,entries in grouped:
        namespace = G.node[term]['namespace']
        root = G.graph['roots'][namespace]
        for path in nx.simple_paths.all_simple_paths(G, term, root):
            for n in path:
                node = G.node[n]
                node['background'] = node['background'].union(entries)

def calculate_pvalues(G, query, min_category_size=2):
    """ calculate pvalues for all categories in the graph

    :param min_category_size: categories smaller than this number are ignored, default : 2
    :returns: dictionary of term : pvalue
    """
    pvalues = {}
    N = len(query)
    for i in G:
        node = G.node[i]
        background = node.get('background', None)
        if background is None:
            continue
        n = len(background)
        if n < min_category_size:
            continue
        node['n'] = n
        hits = query.intersection(background)
        x = len(hits)
        if x == 0:
            continue
        else:
            node['query'] = query
            node['N'] = N
            node['hits'] = hits
            node['x'] = x
            M, n = node['M'], node['n']
            p = hypergeom.sf(x, M, n, N)
            node['p'] = p
            pvalues[i] = p
    return pvalues


def multiple_testing_correction(G, pvalues, alpha=0.05, method='benjamini-hochberg'):
    """ correct pvalues for multiple testing and add corrected `q` value
    :param alpha: significance level default : 0.05
    :param method: multiple testing correction method [bonferroni|benjamini-hochberg]
    """
    G.graph.update({ 'multiple-testing-correction': method,
        'alpha' : alpha })
    if method == 'bonferroni':
        n = len(pvalues.values())
        for term,p in pvalues.items():
            node = G.node[term]
            q = p * n
            node['q'] = q
            node['significant'] = q < 0.05
    elif method == 'benjamini-hochberg':
        terms, ps = zip(*pvalues.items())
        rejs, qs = fdrcorrection(ps, alpha)
        for term, q, rej in zip(terms, qs, rejs):
            node = G.node[term]
            node['q'] = q
            node['significant'] = rej
    else:
        raise ValueError(method)

def filter_significant(G):
    """ get significant terms"""
    sig = [n for n in G if G.node[n].get('significant', False)]
    return sig
