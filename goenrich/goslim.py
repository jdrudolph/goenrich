"""
tools for working with goslims
"""
import networkx as nx

def add(O, goslim, nodes):
    """ add goslim to specified nodes in the ontology """
    for n in nodes:
        O.node[n]['subset'].setdefault(set()).add(goslim)

def subset(O, goslim):
    """ get the ontology-subset corresponding to the specified goslim

    :param goslim: specify a goslim which the ontolgy is filtered for
    """
    if goslim is not None and goslim not in O.graph['goslims']:
        raise ValueError('goslim {} is not part of the ontology definition'.format(goslim))
    goslim_nodes = [(n,data) for n,data in O.nodes(data=True)
            if goslim in data.get('subset', set())]
    G = O.subgraph(n for n,_ in goslim_nodes)
    for term, node in goslim_nodes:
        root = G.graph['roots'][node['namespace']]
        nodes = [n for path in nx.all_simple_paths(O, term, root)
                for n in path if goslim in O.node[n].get('subset', set())]
        G.add_edges_from(e for e in zip(nodes, nodes[1:]))
    return G

def read(filename):
    """ read .obo file assuming all 'id: GO:XXXXXXX' belong to the
    goslim

    :returns: list of go terms found in the file """
    findid = re.compile('^id: (GO:\d+)')
    with open(filename) as f:
        for line in f:
            m = findid.match(line)
            if m is not None:
                yield m.groups()[0]
