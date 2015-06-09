import networkx as nx

def add(G, ontology, id, name, namespace, is_a=None, **kwargs):
    """ add term to ontology graph """
    if namespace != ontology or kwargs.get('def', '').startswith('OBSOLETE'):
        return
    else:
        if is_a is not None:
            G.add_edge(is_a, id)
        G.add_node(id, name=name)
        return

def term(f, G, ontology):
    """ parse term starting after [Term] tag, until key: value pair is missed """
    attr = {}
    while True:
        line = f.readline()
        try:
            key,value = line.split('!')[0].strip().split(': ', 1) # remove comments starting with !
            attr[key] = value
        except ValueError as e: # term done, no more key-value-pairs found
            add(G, ontology, **attr)
            return

filename = 'db/go-basic.obo'
ontology = 'biological_process'

def graph(filename, ontology):
    """ Generate ontology graph """
    G = nx.DiGraph(name=ontology)
    with open(filename) as f:
        while True:
            line = f.readline()
            if line == '[Term]\n': # start term
                term(f, G, ontology)
            elif line == '': # entire file parsed
                break
    return G
