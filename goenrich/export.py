import networkx as nx
import pandas as pd

import goenrich

def to_frame(G, node_filter = lambda node: True, **kwargs):
    """ export enrichment graph to pd.DataFrame

    :param node_filter: decision function based with access to the node data dictionary
    """
    return (pd.DataFrame([
        {k: v for d in [{'term':term}, node] for k,v in d.items()}
        for term, node in G.nodes(data=True) if node_filter(node)])
        .set_index('term'))

def to_graphviz(G, sig, gvfile, graph_label=None, **kwargs):
    """ export graph of signifcant findings to dot file.
    A png can be generated from the commandline using graphviz

    dot -Tpng filpath.dot > filepath.png

    :param sig: array_like of node lables to include in result graph
    :param gvfile: file or filepath
    :param graph_label: give custom graph label otherwise
        additional information will be printed.
        For empty label pass graph_label=''.
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
        if 'q' in node:
            attr['color'] = 'red' if node['significant'] else 'black'
            attr['label'] = """{name}
            {x} / {n} genes
            q = {q:.5f}""".format(name=node['name'], q=node['q'], x=node['x'], n=node['n'])
        else:
            attr['color'] = 'black'
            attr['label'] = """{name}""".format(name=node['name'])
        R.node[n] = attr

    A = nx.to_agraph(R)
    if graph_label is not None:
        A.graph_attr['label'] = graph_label
    else:
        A.graph_attr['label'] = 'multiple testing correction: {}\nat alpha={}'.format(
                    G.graph['multiple-testing-correction'], G.graph['alpha'])
    A.graph_attr['labelloc'] = 't'
    
    if hasattr(gvfile, 'write'):
        A.write(gvfile)
    else:
        with open(gvfile, 'w') as f:
            A.write(f)

