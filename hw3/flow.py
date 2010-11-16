#!/usr/bin/python
import igraph, numpy, sys, random, pysparse
from igraph import *
from numpy import *
from pysparse import spmatrix
from pysparse import precon
from pysparse import itsolvers
from pysparse.itsolvers import *

def get_L(graph, size):
    laplacian = zeros((size,size))

    #laplacian == D - A
    adj_list = graph.get_adjlist()
    for i in range(size):
        for j in adj_list[i]:
            if i != j:
                laplacian[i][j] = -1.0
                laplacian[j][i] = -1.0
        laplacian[i][i] = int( graph.vs[i]["original_num"] )

    return laplacian.copy()

def get_flow(graph, W, size):
    b = zeros(size)

    #calculate b. go through all nodes in G
    for i in range(size):
        #sum up flow coming out of W
        for node in W:
            if i != node:
                try:
                    graph.get_eid(i,node)
                    #add in flow if edge exists
                    b[i] += int(graph.vs[node]["original_num"])
                except:
                    pass
    return b

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

    #create Laplacian of graph
    L = get_L(graph, size)

    #create b(x) -- flow coming out of set W
    b = get_flow(graph, W, size)

    #solve for u(x)
    A = spmatrix.ll_mat_sym(size)
    for i in range(size):
        for j in range(size):
            if j <= i:
                A[i,j] = L[i][j]
    walk = None
    u_x = numpy.empty(size)
    info, iter_iter, relres = pcg(A.to_sss(),b,u_x,1e-12,10000)
    A = None
    print "%s : %s : %s" % (info, iter_iter, relres)

    #calculate error in between two functions
    error = 0
    for node in graph.vs:
        error += pow(int(node["original_num"]) - u_x[node.index], 2)
    error = sqrt(error)
    print error

main()
