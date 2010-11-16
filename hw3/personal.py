#!/usr/bin/python
import igraph, numpy, sys, random, pysparse
from igraph import *
from numpy import *
from pysparse import spmatrix
from pysparse import precon
from pysparse import itsolvers
from pysparse.itsolvers import *

def get_walk(graph, degree):
    size = len(graph.vs)
    walk = zeros((size,size))
    adj_list = graph.get_adjlist()
    for i in range(size):
        for j in adj_list[i]:
            walk[i][j] = 1.0
            walk[j][i] = 1.0

    degree_inv = zeros(size)
    for i in range(size):
        degree_inv[i] = 1.0 / degree[i]
    for i in range(size):
        for j in range(size):
            walk[j][i] *= degree_inv[i]
    
    return walk

def get_conductance(graph,nodes,d_V):
    nodes = [int(entry) for entry in nodes]

    #get vertex set and subgraph set to compare differences
    vertices = graph.vs.select(nodes)
    subgraph = graph.subgraph(nodes)

    #get relevant data from vertex set and subgraph
    edges_inside = float(sum(subgraph.degree()))
    total_edges = float(sum(vertices.degree()))

    return (total_edges - edges_inside) / min(d_V - total_edges, total_edges)

def report_conductance(graph,sort_p,alpha):
    lowest = [1e9,1e9]
    size = len(graph.vs)
    d_V = sum(graph.degree())

    for i in range(size):
        conductance = get_conductance(graph, sort_p[:i+1], d_V)
        if conductance < lowest[0]:
            lowest[0] = conductance
            lowest[1] = i+1
    print "Lowest conductance for alpha %s is size %s and conductance %s" % (alpha, lowest[1], lowest[0])

def main():
    alpha = float(sys.argv[1])
    graph = Graph.Read_GraphMLz("wiki.graphmlz")
    graph.to_undirected()
    self_loops = [edge.index for edge in graph.es if edge.source == edge.target]
    graph.delete_edges(self_loops)
    
    degree = graph.degree()
    size = len(graph.vs)

    #create X(u)
    chi_u = zeros(size)
    chi_u[int(random.random()*(size-1))] = 1.0

    #transform walk and X(u) to find personal pagerank
    walk = get_walk(graph, degree)
    walk *= (1-alpha)
    walk = identity(size) - walk
    chi_u *= alpha

    #find p(u)
    A = spmatrix.ll_mat_sym(size)
    for i in range(size):
        for j in range(size):
            if j <= i:
                A[i,j] = walk[i][j]
    walk = None
    p_u = numpy.empty(size)
    info, iter_iter, relres = pcg(A.to_sss(),chi_u,p_u,1e-12,10000)
    A = None
    print "%s : %s : %s" % (info, iter_iter, relres)

    #find conductance by creating q(u) = p(u) / d(u)
    q_u = p_u.copy()
    for index in range(len(q_u)):
        q_u[index] /= degree[index]
    sort_q = list(argsort(q_u))
    sort_q.reverse()
    report_conductance(graph, sort_q, alpha)

    #find set T from sorted p(u)
    well_spread = True
    sort_p = list(argsort(p_u))
    sort_p.reverse()

    #calculate limit val
    d_T = 0.0
    d_V = sum(degree)
    for i in range(size/2):
        d_T += degree[sort_p[i]]
    limit = (3.0*d_T) / (2.0*d_V)

    #report if p(u) is well spread
    for i in range(size/2):
        if p_u[sort_p[i]] > limit:
            well_spread = False
            break

    print "p(u) with alpha %s is well spread? %s" % (alpha, well_spread)

main()
