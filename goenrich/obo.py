import networkx as nx

def add(G, id, name, namespace, is_a=None, **kwargs):
    """ add term to ontology graph """
    if kwargs.get('def', '').startswith('"OBSOLETE'):
        return 'obsolete'
    else:
        if is_a is not None:
            G.add_edge(id, is_a) # child -> parent
        G.add_node(id, name=name, namespace=namespace)
        if name == namespace:
            G.graph['roots'][name] = id
        return 'added'

def term(f, G):
    """ parse term starting after [Term] tag, until key: value pair is missed """
    attr = {}
    while True:
        line = f.readline()
        if line == '\n': # end of term found
            return add(G, **attr)
        else:
            # remove comments and split to `key: value`
            key,value = line.split('!')[0].strip().split(': ', 1)
            attr[key] = value

def graph(filename, verbose=False):
    """ Generate ontology graph """
    G = nx.DiGraph(roots={})
    i = 0
    obsolete = 0
    with open(filename) as f:
        while True:
            line = f.readline()
            if line == '[Term]\n': # start term
                i += 1
                if term(f, G) == 'obsolete':
                    obsolete += 1
            elif line == '': # entire file parsed
                break
    if verbose:
        print(i, 'terms parsed,', obsolete, 'obsolete ignored')
    return G
