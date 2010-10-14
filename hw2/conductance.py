#!/usr/bin/python

import sys,re
from igraph import *

def find_conductance(graph, name):
    #convert to undirected and remove self-loops
    graph.to_undirected()
    print(graph)
    self_loops = [edge.index for edge in graph.es if edge.source == edge.target]
    graph.delete_edges(self_loops)

    #extract the nodes of interest from graph
    node_list = graph[name]
    nodes = re.split(', ', node_list)
    nodes = [int(entry) for entry in nodes]

    #get vertex set and subgraph set to compare differences
    vertices = graph.vs.select(nodes)
    subgraph = graph.subgraph(nodes)

    #get relevant data from vertex set and subgraph
    edges_inside = float(sum(subgraph.degree()))
    total_edges = float(sum(vertices.degree()))

    return str((total_edges - edges_inside) / total_edges)

def main():
    if len(sys.argv) < 3:
        sys.exit("Format: conductance.py GRAPH [SET_NAME...]")

    graph = Graph.Read_GraphMLz(sys.argv[1])

    for interest in sys.argv[2:]:
        print "Conductance of \'" + interest + "\': " + find_conductance(graph, interest)

main()
