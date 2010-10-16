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
    if error < epsilon:
        return True
    return False

def main():
    #fix graph up
    graph = Graph.Erdos_Renyi(40,.5)
    graph.to_undirected()
    self_loops = [edge.index for edge in graph.es if edge.source == edge.target]
    graph.delete_edges(self_loops)

    #calculate all initial values
    m = float(len(graph.es))
    v1 = array([degree/(2*m) for degree in graph.degree()])
    print v1
    epsilon = sqrt(dot(v1,v1)) / 1000.0
    print epsilon
    random_nodes = [int(random.random()*len(graph.vs)) for i in range(10)]

    #initialize p0 to start in 10 random nodes
    p = arange(len(graph.vs))
    for i in range(len(graph.vs)):
        p[i] = 0
        if i in random_nodes:
            p[i] = 1
    p = p / sqrt(dot(p,p))

    #get walk matrix from graph
    walk = get_walk(graph,v1)

    #evolve until convergence
    while convergence(p, v1, epsilon) != True:
        p = dot(walk,p)

main()
