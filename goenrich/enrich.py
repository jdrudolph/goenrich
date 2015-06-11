import networkx as nx
import numpy as np
from scipy.stats import hypergeom

def set_background(G, df, entry_id='db_object_id', category_id='go_id'):
    """ Propagate background set through the ontolgy tree
    """
    M = len(df[entry_id].unique()) # total number of objects
    def annotate(i, entries):
        node = G.node[i]
        node['background'] = node.get('background', set([])).union(entries)
        node['M'] = M

    grouped = df.groupby(category_id)[entry_id]
    for term,entries in grouped:
        namespace = G.node[term]['namespace']
        root = G.graph['roots'][namespace]
        for path in nx.simple_paths.all_simple_paths(G, term, root):
            for n in path:
                annotate(n, entries)

def calculate_pvalues(G, query):
    """ calculate pvalues for all categories in the graph """
    pvalues = {}
    N = len(query)
    for i in G:
        node = G.node[i]
        background = node.get('background', None)
        if background is None:
            continue
        n = len(background)
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


def multiple_testing_correction(G, pvalues, alpha=0.05, method='bonferroni'):
    """ correct pvalues for multiple testing and add corrected `q` value """
    if method == 'bonferroni':
        G.graph['multiple-testing-correction'] = 'bonferroni'
        n = len(pvalues.values())
        for term,p in pvalues.items():
            node = G.node[term]
            q = p * n
            node['q'] = q
            node['significant'] = q < 0.05
    else:
        raise ValueError(method)

def filter_significant(G, alpha=0.05):
    """ get significant terms according to q-values at level alpha """
    sig = [n for n in G if G.node[n].get('q', 1) < alpha]
    return sig
