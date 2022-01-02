from math import inf
import random as random
import networkx as nx 
import matplotlib.pyplot as plt


def karger(graph, edgeMap):
    '''
    randomly selects an edge and merges its nodes into a single node
    also returns map for relabelling graph
    '''
    map={}
    while graph.number_of_nodes() > 2:
        n1, n2 = random.choice(list(graph.edges()))
        graph, map = merge(graph, n1, n2, edgeMap, self_loops = False)
    return graph, map

def merge(G, u, v, mapping, self_loops=True):
    '''
    merge function which merges two nodes and creates node mapping dictionary
    '''
    mapping[int(str(u)[0])] += str(v)
    mapping[int(str(u)[0])] = ''.join(sorted(mapping[int(str(u)[0])]))
    mapping[int(str(v)[0])] += str(u)
    mapping[int(str(v)[0])] = ''.join(sorted(mapping[int(str(v)[0])]))

    remappingEdges = G.edges(v, data=True)
    remappingEdges = list(remappingEdges)

    v_data = G.nodes[v]
    G.remove_node(v)

    for (previousW, previousX, d) in remappingEdges:
        if previousW != v:
            w = previousW  
        else:
            w = u
        if previousW != v:
            x = previousW  
        else:
            x = u
        x = previousX if previousX != v else u

        if ({previousW, previousX} == {u, v}) and not self_loops:
            continue

        if not G.has_edge(w, x) or G.is_multigraph():
            G.add_edge(w, x, **d)
        

    if "contraction" in G.nodes[u]:
        G.nodes[u]["contraction"][v] = v_data
    else:
        G.nodes[u]["contraction"] = {v: v_data}

    return G, mapping



def map_fill(map):
    '''
    map fill function to fill mapping var for merged nodes. 
    updates mapping dictionary for relabelling merged nodes
    '''
    for k,v in map.items():
        for s in v:
            v = v.replace(s, map[int(s)])
            v = ''.join(sorted(list(set(list(v)))))
            map[k] = v
    return map


nodeList = [(0,1),(0,2),(0,3),(0,4),(1,2),(1,3),(1,4),(2,3),(2,4),(3,4),(1,5),(4,6),(5,6),(5,7),(5,8),(6,7),(6,8),(7,8)]
G = nx.MultiGraph()
G.add_edges_from(nodeList)

#option list for graph plot
options = {
    'node_color': 'yellow',
    'node_size': 600,
    'width': 1.5,
    'with_labels': True
}

#display base graph
#nx.draw_circular(G, **options)
#plt.show()
baseMapping = dict(zip(sorted(G), range(0,len(G))))
for k in baseMapping:
    baseMapping[k] = str(baseMapping[k])

#RUNS defines how many rounds of Karger to be run to find min cut
RUNS = 10
minEdges = inf


for i in range(RUNS):
    '''
    run karger algorithm RUNS times and keeps the min cut graph in minRes
    '''
    H = G.copy()
    mapping = baseMapping.copy()
    nE, eM = karger(H, mapping)
    edgeNum = nE.number_of_edges()
    if edgeNum< minEdges:
        minEdges = edgeNum
        minRes = nE
        minMap = eM
    else:
        continue



#updating mapping for edges
minMap = map_fill(minMap)
minMap = map_fill(minMap)

#relabelling graph nodes after merge
minRes = nx.relabel_nodes(minRes, minMap)
edges = minRes.edges()
edges = list(set(edges))[0]
edges = [tuple(edges[0]), tuple(edges[1])]
#print result
print(edges[0], edges[1], minRes.number_of_edges())
#display merged graph
nx.draw_circular(minRes, **options)
plt.show()