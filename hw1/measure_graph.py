#!/usr/bin/python

import os,sys,igraph,math

from igraph import *

#Calculate assortativity
#igraph doesn't have assortativity calculation
#found one online @ snipplr.com
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
    file = open("test.graphml", 'r')

    #get the graph from my edgelist file
    graph = Graph.Read_GraphML(file)
    print(graph)
    print "Assortativity: " + str(assortativity(graph)) + "\n"
    
    #The transitivity measures the probability that two neighbors of a vertex are connected.
    #In case of the average local transitivity this probability if calculated for each vertex 
    #and then the average is taken for those vertices which have at least two neighbors.
    #If there are no such vertices then NaN is returned. 
    print "C(2) clustering: " + str(graph.transitivity_avglocal_undirected()) + "\n"

main()
