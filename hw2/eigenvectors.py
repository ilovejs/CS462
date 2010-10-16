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
        degree_inv[i][i] = 1.0 / sqrt(degrees[i])

    #return symmetric lazy walk matrix
    identity = zeros((len(u1),len(u1)))
    return .5*(dot(dot(degree_inv,adjacency),degree_inv) + identity)

def get_eigv2(graph, v2):
    #create adjacency
    adjacency = zeros((len(v2),len(v2)))
    adj_list = graph.get_adjlist()
    for i in range(len(v2)):
        for j in adj_list[i]:
            adjacency[i][j] = 1.0
            adjacency[j][i] = 1.0

    #create inverse degree matrix D^(-1/2)
    degree_inv = zeros((len(v2),len(v2)))
    degrees = graph.degree()
    for i in range(len(degrees)):
        degree_inv[i][i] = 1.0 / degrees[i]

    identity = zeros((len(v2),len(v2)))
    walk = .5*(dot(adjacency,degree_inv) + identity)
    result_v = dot(walk,v2)
    return result_v / v2

def convergence(old_x, x):
    #set up lambda and mu from the ratio
    ratio_vector = x / old_x
    lambda_val = ratio_vector.max()
    mu = 1 - lambda_val

    #check all values for convergence
    converged = True
    epsilon = 1e-9
    for i in range(len(x)):
        if abs(x[i] - (lambda_val*old_x[i])) > (mu*old_x[i]) + epsilon:
            converged = False
            break

    return converged

def approximate_u2(x, lazy_walk, u1):
    #do calculation from PS2
    x = x - (dot(u1,x)*u1)
    x = x / (sqrt(dot(x,x)))
    x = dot(lazy_walk,x)
    return x

def get_u2(x, lazy_walk, u1):
    #start convergence, save x for comparison
    old_x = x.copy()
    x = approximate_u2(x, lazy_walk, u1)

    #iterate until convergence
    while convergence(old_x, x) != True:
        old_x = x.copy()
        x = approximate_u2(x, lazy_walk, u1)

    return x

def get_cheegers(v2):
    argsort_v2 = argsort(v2)

    cheeger_sets = []
    for i in range(len(argsort_v2))[:0:-1]:
        cheeger_sets.append(list(argsort_v2[len(argsort_v2):i-1:-1]))

    return cheeger_sets

def conductance(graph,nodes):
    #odd result if I don't convert to int
    nodes = [int(node) for node in nodes]

    #get vertex set and subgraph set to compare differences
    vertices = graph.vs.select(nodes)
    subgraph = graph.subgraph(nodes)

    #get relevant data from vertex set and subgraph
    edges_inside = float(sum(subgraph.degree()))
    total_edges = float(sum(vertices.degree()))

    return (total_edges - edges_inside) / total_edges

def main():
    #graph = Graph.Read_GraphMLz(sys.argv[1])
    graph = Graph.Erdos_Renyi(40,.5)
    graph.to_undirected()
    self_loops = [edge.index for edge in graph.es if edge.source == edge.target]
    graph.delete_edges(self_loops)

    #create D^(1/2) and D^(-1/2) for conversion of vectors
    degrees_inv = array([1 / sqrt(degree) for degree in graph.degree()])
    degrees = array([sqrt(degree) for degree in graph.degree()])

    #implicitly calculate u1, initialize x to random gaussians
    m = float(len(graph.es))
    v1 = array([degree/(2*m) for degree in graph.degree()])
    u1 = degrees_inv*v1
    x = array([random.random() for i in range(len(u1))])

    #create lazy walk matrix and free up memory
    lazy_walk = get_lazy(graph, u1)

    #get u2
    u2 = get_u2(x, lazy_walk, u1)

    #convert to v2 -- D^(1/2) * u2
    v2 = degrees*u2
    eigv_v2 = get_eigv2(graph,v2)

    #calculate conductance using cheeger's inequality
    conductances = []
    v2_c = v2.copy()

    #use D^(1/2) to calculate v2(a) / d(a) for cheeger
    for i in range(len(v2)):
        v2_c[i] = v2_c[i] / (degrees[i]*degrees[i])
    cheeger_sets = get_cheegers(v2_c)

    #find set of lowest conductance
    for nodes in cheeger_sets:
        conductances.append(conductance(graph,nodes))
    lowest = min(conductances)
    print conductances

main()
