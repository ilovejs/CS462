#!/usr/bin/python
import igraph, numpy, sys, random
from igraph import *
from numpy import *

def print_evaluation(graph,attachment,adamic_adar,jaccard,common_neighbor,shortest_distance):
    #max number of correct edges
    denominator = len(attachment)

    num_attach = 0
    for el in attachment:
        try:
            graph.get_eid(el[0][0],el[0][1])
            num_attach += 1
        except:
            pass

    num_adamic = 0
    for el in adamic_adar:
        try:
            graph.get_eid(el[0][0],el[0][1])
            num_adamic += 1
        except:
            pass

    num_jaccard = 0
    for el in jaccard:
        try:
            graph.get_eid(el[0][0],el[0][1])
            num_jaccard += 1
        except:
            pass

    num_common = 0
    for el in common_neighbor:
        try:
            graph.get_eid(el[0][0],el[0][1])
            num_common += 1
        except:
            pass

    num_distance = 0
    for el in shortest_distance:
        try:
            graph.get_eid(el[0],el[1])
            num_distance += 1
        except:
            pass

    print "Preferential attachment: %s\nAdamic/Adar: %s\nJaccard: %s \
            \nCommon Neighbor: %s\nDistance: %s" \
            % (num_attach/float(denominator),num_adamic/float(denominator), \
            num_jaccard/float(denominator),num_common/float(denominator), \
            num_distance/float(denominator))

def main():
    #load graph, clean it up
    graph = Graph.Read_GraphMLz("wiki.graphmlz")
    graph.to_undirected()
    self_loops = [edge.index for edge in graph.es if edge.source == edge.target]
    graph.delete_edges(self_loops)

    #get the edgelist and pick 1000 unique random edges
    edge_list = graph.get_edgelist()
    edge_set = set()
    node_set = set()
    while len(edge_set) < 1000:
        index = random.randint(0,len(edge_list))
        edge_set.add(edge_list[index])

    #find all unique nodes used in random edges
    for edge in edge_set:
        node_set.add(edge[0])
        node_set.add(edge[1])

    edge_list = list(edge_set)
    nodes = sorted(list(node_set))

    #retrieve the subgraph over those nodes
    g_training = graph.subgraph(nodes)

    #find n (difference between true # of edges in subgraph
    #and number that we are training from (1000))
    n = len(g_training.es) - len(edge_list)

    #remove edges that g_training shouldn't know about
    to_delete = []
    full_list = g_training.get_edgelist()
    for edge in full_list:
        try:
            edge_list.index(edge)
        #delete edge if it doesn't exist in our edge_list
        except:
            to_delete.append(edge)

    #get the edge ids of all the edges to delete, and delete them
    eids = []
    for edge in to_delete:
        eids.append(g_training.get_eid(edge[0],edge[1]))
    g_training.delete_edges(eids)

    #update node ids for g_training
    nodes = range(len(g_training.vs))

    #shortest distance
    scores = []
    #returns length of shortest path from all nodes to all nodes
    #where nodes are the nodes we care about
    path_lengths = g_training.shortest_paths_dijkstra(nodes,mode=ALL)
    for x in nodes:
        #this loop just makes sure we don't double count
        for y in [node for node in nodes if node > x]:
            #if the edge exists in g_training, don't add it
            try:
                g_training.get_eid(x,y)
            except:
                #add all paths of length 2
                if path_lengths[x][y] == 2:
                    scores.append((x,y))

    #pick edges to predict
    predictions = set()
    while len(predictions) < n:
        index = random.randint(0,len(scores))
        predictions.add(scores[index])
    shortest_distance = list(predictions)

    #create neighbor list for all nodes we care about
    neighbors = {}
    for el_id in nodes:
        neighbors[str(el_id)] = []

    for i in range(len(nodes)):
        for j in range(len(nodes)):
            if i != j:
                #if edge exists in g_training, add to neighbors
                try:
                    g_training.get_eid(i,j)
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
                #score is just the intersection
                score = len(x_set & y_set)
                scores.append(((x,y),score))


    scores = sorted(scores, key=lambda score: score[1], reverse=True)
    common_neighbor = scores[:n]

    #Jaccard
    scores = []
    for x in nodes:
        x_set = set(neighbors[str(x)])
        for y in [node for node in nodes if node > x]:
            try:
                edge_list.index((x,y))
            except:
                y_set = set(neighbors[str(y)])
                #score is intersection over union
                numerator = len(x_set & y_set)
                denominator = len(x_set | y_set)
                if denominator != 0:
                    score = float(numerator) / float(denominator)
                if denominator == 0:
                    score = 0

                scores.append(((x,y),score))

    scores = sorted(scores, key=lambda score: score[1], reverse=True)
    jaccard = scores[:n]

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
                #score is sum 1/log(neighbors' neighbors)
                for feature in features:
                    score += 1.0 / log(len(neighbors[str(feature)]))

                scores.append(((x,y),score))

    scores = sorted(scores, key=lambda score: score[1], reverse=True)
    adamic_adar = scores[:n]

    #Preferential Attachment
    scores = []
    for x in nodes:
        x_set = set(neighbors[str(x)])
        for y in [node for node in nodes if node > x]:
            try:
                edge_list.index((x,y))
            except:
                y_set = set(neighbors[str(y)])
                #score is multiplication of size of neighbor sets
                score = len(x_set) * len(y_set)

                scores.append(((x,y),score))

    scores = sorted(scores, key=lambda score: score[1], reverse=True)
    attachment = scores[:n]

    print_evaluation(graph,attachment,adamic_adar,jaccard,common_neighbor,shortest_distance)

main()
