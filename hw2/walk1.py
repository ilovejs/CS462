#!/usr/bin/python
import numpy, igraph, sys
from igraph import *
from numpy import *

def get_walk(graph,v1):
    #create adjacency
    walk = zeros((len(v1),len(v1)))
    adj_list = graph.get_adjlist()
    for i in range(len(v1)):
        for j in adj_list[i]:
            walk[i][j] = 1.0
            walk[j][i] = 1.0

    #create inverse degree matrix D^(-1)
    degree_inv = zeros(len(v1))
    degrees = graph.degree()
    for i in range(len(degrees)):
        degree_inv[i] = 1.0 / degrees[i]
    for i in range(len(v1)):
        for j in range(len(v1)):
                walk[j][i] *= degree_inv[i]

    return walk

def convergence(p, v1, epsilon):
    difference = p - v1
    error = sqrt(dot(difference,difference))
    if error < epsilon:
        return True
    return False

def get_conductances(graph,v2):
    #sort by values by argument value (index of node)
    argsort_v2 = argsort(v2)
    sorted_nodes = [int(el) for el in argsort_v2]

    #get sets of highest v2(a)/d(a) value (up to half set size)
    conductances = []
    for i in range(len(sorted_nodes)/2):
        conductances.append(conductance(graph,sorted_nodes[:i+1]))

    return conductances

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
    graph = Graph.Read_GraphMLz(sys.argv[1])
    graph.to_undirected()
    self_loops = [edge.index for edge in graph.es if edge.source == edge.target]
    graph.delete_edges(self_loops)
    degrees = graph.degree()

    #calculate all initial values
    m = float(len(graph.es))
    v1 = array([float(degree)/(2.0*m) for degree in degrees])
    epsilon = sqrt(dot(v1,v1)) / 1000.0
    random_node = int(random.random()*len(graph.vs))

    #initialize p0 to start in 10 random nodes
    p = zeros(len(graph.vs))
    for i in range(len(graph.vs)):
        p[i] = 0.0
        if i == random_node:
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
        conductances.append(min(get_conductances(graph,p_c)))
    print "Conductances when walking from node " + str(random_node) + ": " + conductances

main()
