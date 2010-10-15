#!/usr/bin/python
import numpy, igraph
from igraph import *
from numpy import *

def get_lazy(graph, u1):
    #create adjacency 
    adjacency = zeros((len(u1),len(u1)))
    adj_list = graph.get_adjlist()
    for i in range(len(u1)):
        for j in adj_list[i]:
            adjacency[i][j] = 1.0
            adjacency[j][i] = 1.0

    #create inverse degree matrix D^(-1/2)
    degree_inv = zeros((len(u1),len(u1)))
    degrees = graph.degree()
    for i in range(len(degrees)):
        degree_inv[i][i] = 1 / sqrt(degrees[i])

    #return symmetric lazy walk matrix
    identity = zeros((len(u1),len(u1)))
    return .5*(dot(dot(degree_inv,adjacency),degree_inv) + identity)

def approximate_u2(x, lazy_walk, u1):
    #do calculation from PS2
    x = x - (dot(u1,x)*u1)
    x = x / (sqrt(dot(x,x)))
    x = dot(lazy_walk,x)
    return x

def convergence(old_x, x):
    #set up lambda and mu from the ratio
    ratio_vector = x / old_x
    lambda_val = ratio_vector.max()
    mu = 1 - lambda_val

    #check all values for convergence
    converged = True
    for i in range(len(x)):
        if abs(x[i] - (lambda_val*old_x[i])) > (mu*old_x[i]):
            converged = False
            break

    return converged

def get_u2(x, lazy_walk, u1):
    #start convergence, save x for comparison
    old_x = x.copy()
    x = approximate_u2(x, lazy_walk, u1)

    #iterate until convergence
    while convergence(old_x, x) != True:
        old_x = x.copy()
        x = approximate_u2(x, lazy_walk, u1)

    return x

def main():
    #graph = Graph.Read_GraphMLz(sys.argv[1])
    graph = Graph.Erdos_Renyi(40,.5)
    graph.to_undirected()
    print(graph)

    #implicitly calculate u1, initialize x to random gaussians
    m = float(len(graph.es))
    u1 = array([degree/(2*m) for degree in graph.degree()])
    x = array([random.random() for i in range(len(u1))])

    #create lazy walk matrix and free up memory
    lazy_walk = get_lazy(graph, u1)
    graph = None

    #get u2
    u2 = get_u2(x, lazy_walk, u1)
    print u2

    #convert to v2 -- D^(1/2) * u2
    #degrees = array([sqrt(degree) for degree in graph.degree()])
    #v2 = degrees*u2

main()
