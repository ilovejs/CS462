#!/usr/bin/python
import igraph, numpy, scipy, sys, random
from igraph import *
from numpy import *
from scipy import *

def main():
    graph = Graph.Read_GraphMLz("wiki.graphmlz")
    graph.to_undirected()
    self_loops = [edge.index for edge in graph.es if edge.source == edge.target]
    graph.delete_edges(self_loops)

    percentage = float(sys.argv[1])
    size = len(graph.vs)

    #create set W, with |W| = percentage*|V|
    W = set([])
    while len(W) < percentage*size:
        random_node = random.random()*(size-1)
        W.add(int(random_node))
    W = list(W)

    #calculate the mean of W -- u(x)
    size_W = len(W)
    sum_W = sum([int(graph.vs[node]["original_num"]) for node in W])
    mean_W = sum_W / size_W

    #calculate error in mean function
    error = 0
    for node in graph.vs:
        error += pow(int(node["original_num"]) - mean_W, 2)
    error = sqrt(error)

    print error

main()
