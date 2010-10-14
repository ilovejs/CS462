#!/usr/bin/python

import sys,igraph,string,re

from igraph import *

def main():
    #get the graph from my edgelist file
    graph = Graph.Read_Edgelist("edge_list")
    titles = open("/home/dougvk/Downloads/titles-sorted.txt",'r').xreadlines()


    #add metadata to graph
    i = 1
    for line in titles:
        if i < 5711323: #stop after all the nodes have been covered
            line = str(line)[:len(line)-1].lower()
            graph.vs[i]["title"] = line
            graph.vs[i]["original_num"] = str(i) 
            i += 1

    #remove all useless vertices
    seq = graph.vs.select(_degree = 0)
    graph.delete_vertices(seq)

    #sanitize string
    valid_chars = "-_ %s%s" % (string.ascii_letters, string.digits)

    #set up a keyword dictionary for identifying interesting sets later
    key_dict = {}
    i = 0
    for vertex in graph.vs:
        title = vertex["title"]

        #sanitze title and add keywords to dictionary
        if title != None or title == "":
            title = ''.join(char for char in title if char in valid_chars)
        else:
            title = ""
        keywords = re.split('[_-]',title)
        for word in keywords:
            if len(word) > 2:
                if word in key_dict:
                    key_dict[word.lower()].append(i)
                if word not in key_dict:
                    key_dict[word.lower()] = [i]
        i += 1

    #add keyword,nodelist to graph
    for key in key_dict.keys():
        graph[key] = str(key_dict[key])[1:-1]

    print(graph)
    graph.write_graphmlz("wiki.graphmlz")

main()
