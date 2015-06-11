import networkx as nx

def to_graphviz(G, sig, filepath):
    """ export graph of signifcant findings to dot file.
    A pdf can be generated from the commandline using graphviz

    dot -Tpdf filpath.dot > filepath.pdf
    """
    nodes = set([])
    for n in sig:
        namespace = G.node[n]['namespace']
        root = G.graph['roots'][namespace]
        for path in nx.simple_paths.all_simple_paths(G, n, root):
            nodes.update(path)
    R = G.subgraph(nodes).reverse()
    R.graph = {'rankdir' : 'TB'}
    for n in R:
        node = R.node[n]
        attr = {}
        attr['shape'] = 'record'
        attr['color'] = 'red' if node['significant'] else 'black'
        attr['label'] = """{name}
        {x} / {n} genes
        q = {q:.5f}""".format(name=node['name'], q=node['q'], x=node['x'], n=node['n'])
        R.node[n] = attr
    A = nx.to_agraph(R)
    with open(filepath, 'w') as f:
        A.write(f)

