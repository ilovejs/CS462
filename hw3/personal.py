#!/usr/bin/python
import igraph, numpy, scipy, sys
from igraph import *
from numpy import *
from scipy import *
from scipy.sparse import linalg
from scipy.sparse.linalg import *

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

def main():
    alpha = float(sys.argv[1])
    graph = Graph.Erdos_Renyi(40,.5)
    degree = graph.degree()
    size = len(graph.vs)

    #create X(u)
    chi_u = zeros(size)
    chi_u[size/2] = 1.0

    #transform walk and X(u) to find personal pagerank
    walk = get_walk(graph, degree)
    walk *= (1-alpha)
    walk = identity(size) - walk
    chi_u *= alpha

    #find p(u)
    answer = cg(walk,chi_u,tol=1e-9)[0]
    #report_conductance(graph, answer, alpha)

    #find set T from sorted p(u)
    well_spread = True
    sort_ans = list(argsort(answer))
    sort_ans.reverse()

    #calculate limit val
    d_T = 0.0
    d_V = sum(degree)
    for i in range(size/2):
        d_T += degree[sort_ans[i]]
    limit = (3.0*d_T) / (2.0*d_V)

    #report if p(u) is well spread
    for i in range(size/2):
        if answer[sort_ans[i]] > limit:
            well_spread = False
            break

    print answer
    print dot(walk,answer)

main()
