import re
import os
import pickle
import networkx as nx

def add(G, id, name, namespace, is_a=None, subset=None, **kwargs):
    """ add term to ontology graph """
    if next(iter(kwargs.get('def', set([''])))).startswith('"OBSOLETE'):
        return 'obsolete'
    else:
        # assumed unique
        id = next(iter(id))
        name = next(iter(name)) 
        namespace = next(iter(namespace)) 
        if is_a is not None:
            for parent in is_a:
                G.add_edge(id, parent)
        attr_dict = {}
        if subset is not None:
            attr_dict['subset'] = subset
        G.add_node(id, name=name, namespace=namespace, attr_dict=attr_dict)
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
            attr.setdefault(key, set()).add(value)

def graph(filename, verbose=False, ontology_cache=None):
    """ Generate ontology graph
    
    :param filename: .obo file name
    :param verbose: print parsing info
    :param ontology_cache: pickle graph to file for faster loading"""
    if ontology_cache is not None:
        if os.path.isfile(ontology_cache):
            with open(ontology_cache, 'rb') as f:
                return pickle.load(f)
    G = nx.DiGraph(roots={})
    i = 0
    obsolete = 0
    goslim_definition = re.compile('subsetdef: (goslim_\w+) "(.*)"')
    with open(filename) as f:
        while True:
            line = f.readline()
            match = re.match(goslim_definition, line)
            if match is not None:
                G.graph.setdefault('goslims', {}).update(dict([match.groups()]))
            # TODO regex
            if line == '[Term]\n': # start term
                i += 1
                if term(f, G) == 'obsolete':
                    obsolete += 1
            elif line == '': # entire file parsed
                break
    if verbose:
        print(i, 'terms parsed,', obsolete, 'obsolete ignored')

    Grev = G.reverse()
    for root in G.graph['roots'].values():
        G.node[root]['depth'] = 0
        for n, depth in nx.single_source_shortest_path_length(Grev, root).items():
            G.node[n]['depth'] = depth

    if ontology_cache is not None:
        with open(ontology_cache, 'wb') as f:
            pickle.dump(G, f)
    return G
