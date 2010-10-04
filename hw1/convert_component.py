#!/usr/bin/python

import re,sys,math,os,igraph
from igraph import *

# matches the node and the list it points to
nodelist = re.compile(r'\s+(\d+)\|\d+\|(.*)')

# adds the edges into the graph from the node: outlink;...;outlink file
def create_edges(line, graph):
    list = nodelist.search(line)
    node = list.group(1)
    node = int(node)
    outlinks = list.group(2).split(';')
    if len(outlinks) == 1 and outlinks[0] == '':
        return
    for link in outlinks:
        link = int(link)
        graph.add_edges([(node,link)])


def main():
    # make a graph of 6 million nodes
    graph = Graph(6000000)
    graph.to_directed()
    titles = open("titles-sorted.txt",'r').xreadlines()

    # for each node, add its title and original node number
    # (node number gets remapped after the deletion process)
    i = 1
    for line in titles:
        line = str(line)
        graph.vs[i]["title"] = line[:len(line)-1]
        graph.vs[i]["original_num"] = i
        i += 1

    # now go through the component and make all the edges
    lines = open(sys.argv[1], 'r').xreadlines()
    for line in lines:
        create_edges(line,graph)
    
    # delete all vertices with degree 0, output to file
    seq = graph.vs.select(_degree = 0)
    graph.delete_vertices(seq)
    graph.write_graphml("wiki.graphml")

main()
