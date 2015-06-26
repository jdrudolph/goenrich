import numpy as np

def calculate_ES(hits, X_member, X_not_member):
    return np.max(np.cumsum((hits * X_member) + (~hits * X_not_member), axis=0), axis=0)

def gsea_strict(ontology, genes, min_category_size=3, permutations=100, alpha=0.05):
    N = len(genes)
    M = ontology.number_of_nodes() # number of gene sets
    X_member = np.zeros(M)
    X_not_member = np.zeros(M)
    hits = np.zeros((N, M), dtype=bool)
    ignored = 0
    # query all groups
    for i, term in enumerate(ontology):
        background = np.array(list(ontology.node[term]['background']))
        G = len(background)
        if G < min_category_size:
            ignored = ignored + 1
            X_not_member[i] = 0
            X_member[i] = 0
        else:
            hits[:,i] = np.in1d(genes, background, assume_unique=True)
            X_not_member[i] = - np.sqrt(G / (N - G))
            X_member[i] = np.sqrt((N - G) / G)
    print('querying done')
    invalid = (X_member == 0)
    assert invalid.sum() == ignored
    M = M - invalid.sum()
    X_member = X_member[~invalid]
    X_not_member = X_not_member[~invalid]
    hits = hits[:, ~invalid]
    
    ES = calculate_ES(hits, X_member, X_not_member)

    ES_max = np.zeros(permutations)
    for i in range(permutations):
        if i % 10 == 0:
            print('permutation', i)
        random_hits = np.random.permutation(hits)
        ES_max[i] = np.max(calculate_ES(random_hits, X_member, X_not_member))

    ranks = np.zeros(M)
    for i, es in enumerate(ES):
        ranks[i] = (es < ES_max).sum()
    ps = ranks / permutations

    anodes = np.array(G.nodes())
    for n,p in zip(anodes[~invalid], ps):
        node = G.node[n]
        node['p'] = p
        node['significant'] = p < alpha
