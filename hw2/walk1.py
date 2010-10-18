#!/usr/bin/python
import numpy, igraph
from igraph import *
from numpy import *

def get_walk(graph,v1):
    #create adjacency
    adjacency = zeros((len(v1),len(v1)))
    adj_list = graph.get_adjlist()
    for i in range(len(v1)):
        for j in adj_list[i]:
            adjacency[i][j] = 1.0
            adjacency[j][i] = 1.0

    #create inverse degree matrix D^(-1)
    degree_inv = zeros((len(v1),len(v1)))
    degrees = graph.degree()
    for i in range(len(degrees)):
        degree_inv[i][i] = 1.0 / degrees[i]

    walk = dot(adjacency,degree_inv)
    return walk

def convergence(p, v1, epsilon):
    difference = p - v1
    error = sqrt(dot(difference,difference))
    print error
    if error < epsilon:
        return True
    return False

def get_cheegers(p):
    #sort by values by argument value (index of node)
    argsort_p = argsort(p)
    sorted_nodes = [int(el) for el in argsort_p]

    #get sets of highest p(a)/d(a) value (up to half set size)
    cheeger_sets = []
    for i in range(len(sorted_nodes)/2):
        cheeger_sets.append(sorted_nodes[:i+1])

    return cheeger_sets

def get_lowest_conductance(graph,p):
    cheeger_sets = get_cheegers(p)

    #collect conductances, return min
    conductances = []
    for ch_set in cheeger_sets:
        conductances.append(conductance(graph,ch_set))
    return min(conductances)

def conductance(graph,nodes):
    #odd result if I don't convert to int
    nodes = [int(node) for node in nodes]

    #get vertex set and subgraph set to compare differences
    vertices = graph.vs.select(nodes)
    subgraph = graph.subgraph(nodes)

    #get relevant data from vertex set and subgraph
    edges_inside = float(sum(subgraph.degree()))
    total_edges = float(sum(vertices.degree()))

    return (total_edges - edges_inside) / total_edges

def main():
    #fix graph up
    graph = Graph.Erdos_Renyi(40,.5)
    graph.to_undirected()
    self_loops = [edge.index for edge in graph.es if edge.source == edge.target]
    graph.delete_edges(self_loops)
    degrees = graph.degree()

    #calculate all initial values
    m = float(len(graph.es))
    v1 = array([float(degree)/(2.0*m) for degree in degrees])
    epsilon = sqrt(dot(v1,v1)) / 1000.0
    random_nodes = [int(random.random()*len(graph.vs)) for i in range(1)]

    #initialize p0 to start in 10 random nodes
    p = arange(len(graph.vs))
    for i in range(len(graph.vs)):
        p[i] = 0.0
        if i in random_nodes:
            p[i] = 1.0

    #get walk matrix from graph
    walk = get_walk(graph,v1)

    #evolve and collect sets until convergence
    conductances = []
    while convergence(p, v1, epsilon) != True:
        #walk p
        p = dot(walk,p)

        #convert p to p(a)/d(a)
        p_c = p.copy()
        for i in range(len(v1)):
            p_c[i] = p_c[i] / float(degrees[i])
        conductances.append(get_lowest_conductance(graph,p_c))
    print conductances

main()
