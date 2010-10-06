#!/usr/bin/python

import os,sys,igraph,math

from igraph import *

#Calculate assortativity
#igraph doesn't have calculation -- found one online @ snipplr.com
def assortativity(graph):
    degrees = graph.degree()
    degrees_sq = [deg**2 for deg in degrees]

    m = float(graph.ecount())
    num1, num2, den1 = 0, 0, 0
    for source, target in graph.get_edgelist():
        num1 += degrees[source] * degrees[target]
        num2 += degrees[source] + degrees[target]
        den1 += degrees_sq[source] + degrees_sq[target]

    num1 /= m
    den1 /= 2*m
    num2 = (num2 / (2*m)) ** 2

    return (num1 - num2) / (den1 - num2)

def main():
    #get the graph from my edgelist file
    graph = Graph.Read_Edgelist("edge_list")
    titles = open("/home/accts/dev5/Downloads/titles-sorted.txt",'r').xreadlines()
    i = 1

    #add metadata to graph
    for line in titles:
        if i < 5614062: #stop after all the nodes have been covered
            line = str(line)
            graph.vs[i]["title"] = line[:len(line)-1]
            graph.vs[i]["original_num"] = i
            i += 1
    seq = graph.vs.select(_degree = 0)
    graph.delete_vertices(seq)
    print(graph)
    print "Assortativity: " + str(assortativity(graph))
    print "C(2) Clustering: " + str(graph.transitivity_avglocal_undirected())
    graph.write_graphml("wiki.graphml")

main()
