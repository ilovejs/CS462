#!/usr/bin/python

import sys,re
from igraph import *

def find_conductance(graph, name):
    #extract the nodes of interest from graph
    node_list = graph[name]
    nodes = re.split(', ', node_list)
    nodes = [int(entry) for entry in nodes]

    #get vertex set and subgraph set to compare differences
    vertices = graph.vs.select(nodes)
    subgraph = graph.subgraph(nodes)

    #total out edges minus out edges within set
    subgraph_out = sum(subgraph.degree(type="out"))
    select_out = sum(vertices.degree(type="out"))
    actual_out = select_out - subgraph_out

    #edges inside set + edges going out and coming in
    total_edges = len(subgraph.get_edgelist()) + actual_out + sum(vertices.degree(type="in"))

    return str(float(actual_out) / float(total_edges))

def main():
    if len(sys.argv) < 3:
        sys.exit("Format: conductance.py GRAPH [SET_NAME...]")

    graph = Graph.Read_GraphMLz(sys.argv[1])

    for interest in sys.argv[2:]:
        print "Conductance of \'" + interest + "\': " + find_conductance(graph, interest)

main()
