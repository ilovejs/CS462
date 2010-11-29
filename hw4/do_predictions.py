#!/usr/bin/python
import igraph, numpy, sys, random
from igraph import *
from numpy import *

def main():
    graph = Graph.Erdos_Renyi(70,.5)
    graph.to_undirected()
    self_loops = [edge.index for edge in graph.es if edge.source == edge.target]
    graph.delete_edges(self_loops)

    edge_list = graph.get_edgelist()
    edge_set = set()
    node_set = set()
    while len(edge_set) < 1000:
        index = random.randint(0,len(edge_list))
        edge_set.add(edge_list[index])
    for edge in edge_set:
        node_set.add(edge[0])
        node_set.add(edge[1])

    edge_list = list(edge_set)
    nodes = sorted(list(node_set))

    #shortest distance
    scores = []
    path_lengths = graph.shortest_paths_dijkstra(nodes,mode=ALL)
    for x in nodes:
        for y in [node for node in nodes if node > x]:
            try:
                edge_list.index((x,y))
            except:
                if path_lengths[x][y] == 2:
                    scores.append((x,y))

    print scores

    neighbors = {}
    for el_id in nodes:
        neighbors[str(el_id)] = []

    for i in range(len(nodes)):
        for j in range(len(nodes)):
            if i != j:
                try:
                    graph.get_eid(i,j)
                    neighbors[str(i)].append(j)
                except:
                    pass

    #Common Neighbor
    scores = []
    for x in nodes:
        x_set = set(neighbors[str(x)])
        for y in [node for node in nodes if node > x]:
            try:
                edge_list.index((x,y))
            except:
                y_set = set(neighbors[str(y)])
                score = len(x_set & y_set)
                scores.append(((x,y),score))


    scores = sorted(scores, key=lambda score: score[1], reverse=True)
    print scores

    #Jaccard
    scores = []
    for x in nodes:
        x_set = set(neighbors[str(x)])
        for y in [node for node in nodes if node > x]:
            try:
                edge_list.index((x,y))
            except:
                y_set = set(neighbors[str(y)])
                numerator = len(x_set & y_set)
                denominator = len(x_set | y_set)
                if denominator != 0:
                    score = float(numerator) / float(denominator)
                if denominator == 0:
                    score = 0

                scores.append(((x,y),score))

    scores = sorted(scores, key=lambda score: score[1], reverse=True)
    print scores

    #Adamic/Adar
    scores = []
    for x in nodes:
        x_set = set(neighbors[str(x)])
        for y in [node for node in nodes if node > x]:
            try:
                edge_list.index((x,y))
            except:
                y_set = set(neighbors[str(y)])
                features = list(x_set & y_set)
                score = 0
                for feature in features:
                    score += 1.0 / log(len(neighbors[str(feature)]))

                scores.append(((x,y),score))

    scores = sorted(scores, key=lambda score: score[1], reverse=True)
    print scores

    #Preferential Attachment
    scores = []
    for x in nodes:
        x_set = set(neighbors[str(x)])
        for y in [node for node in nodes if node > x]:
            try:
                edge_list.index((x,y))
            except:
                y_set = set(neighbors[str(y)])
                score = len(x_set) * len(y_set)

                scores.append(((x,y),score))

    scores = sorted(scores, key=lambda score: score[1], reverse=True)
    print scores

main()
