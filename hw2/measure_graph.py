#!/usr/bin/python

import os,sys,igraph,math,string

from igraph import *

def main():
    #get the graph from my edgelist file
    graph = Graph.Read_Edgelist("edge_list")
    titles = open("/home/dougvk/Downloads/titles-sorted.txt",'r').xreadlines()

    #sanitize strings
    valid_chars = "-_ %s%s" % (string.ascii_letters, string.digits)

    #add metadata to graph
    i = 1
    for line in titles:
        if i < 5711323: #stop after all the nodes have been covered
            line = str(line)[:len(line)-1]
            title = ''.join(char for char in line if char in valid_chars)
            graph.vs[i]["title"] = title
            graph.vs[i]["original_num"] = i
            i += 1

    #remove all useless vertices
    seq = graph.vs.select(_degree = 0)
    graph.delete_vertices(seq)
    print(graph)
    graph.write_graphmlz("wiki.graphmlz")

main()
