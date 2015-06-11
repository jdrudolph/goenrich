import networkx as nx

def to_graphviz(G, sig, filepath, graph_label=None):
    """ export graph of signifcant findings to dot file.
    A pdf can be generated from the commandline using graphviz

    dot -Tpdf filpath.dot > filepath.pdf

    :param graph_label: give custom graph label otherwise
        additional information will be printed
    """
    nodes = set([])
    for n in sig:
        namespace = G.node[n]['namespace']
        root = G.graph['roots'][namespace]
        for path in nx.simple_paths.all_simple_paths(G, n, root):
            nodes.update(path)
    R = G.subgraph(nodes).reverse()
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
    if graph_label is not None:
        A.graph_attr['label'] = graph_label
    else:
        A.graph_attr['label'] = 'multiple testing correction: {}\nat alpha={}'.format(
                    G.graph['multiple-testing-correction'], G.graph['alpha'])
    A.graph_attr['labelloc'] = 't'
    with open(filepath, 'w') as f:
        A.write(f)

