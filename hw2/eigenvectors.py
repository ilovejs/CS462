#!/usr/bin/python
import numpy, igraph
from igraph import *
from numpy import *

def get_lazy(graph, u1):
    #create adjacency 
    lazy_walk = zeros((len(u1),len(u1)))
    adj_list = graph.get_adjlist()
    for i in range(len(u1)):
        for j in adj_list[i]:
            lazy_walk[i][j] = 1.0
            lazy_walk[j][i] = 1.0

    #create inverse degree matrix D^(-1/2)
    degree_inv = zeros(len(u1))
    degrees = graph.degree()
    for i in range(len(degrees)):
        degree_inv[i] = 1.0 / sqrt(degrees[i])

    #return symmetric lazy walk matrix
    for i in range(len(u1)):
        for j in range(len(u1)):
                lazy_walk[i][j] *= degree_inv[i]
    for i in range(len(u1)):
        for j in range(len(u1)):
                lazy_walk[j][i] *= degree_inv[i]
    return .5*(lazy_walk+identity(len(u1)))

def get_eigv2(graph, v2):
    #create adjacency
    lazy_walk = zeros((len(v2),len(v2)))
    adj_list = graph.get_adjlist()
    for i in range(len(v2)):
        for j in adj_list[i]:
            lazy_walk[i][j] = 1.0
            lazy_walk[j][i] = 1.0

    #create inverse degree matrix D^(-1)
    degree_inv = zeros(len(v2)) 
    degrees = graph.degree()
    for i in range(len(degrees)):
        degree_inv[i] = 1.0 / degrees[i]

    for i in range(len(v2)):
        for j in range(len(v2)):
                lazy_walk[j][i] *= degree_inv[i]
    lazy_walk = .5*(lazy_walk+identity(len(v2)))

    #multiply walk and v2 -- ratio == eigenvalue
    result_v = dot(lazy_walk,v2)
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

def get_conductances(graph,v2):
    #sort by values by argument value (index of node)
    argsort_v2 = argsort(v2)
    sorted_nodes = [int(el) for el in argsort_v2]

    #get sets of highest v2(a)/d(a) value (up to half set size)
    conductances = []
    for i in range(len(sorted_nodes)/2):
        conductances.append(conductance(graph,sorted_nodes[:i+1]))

    return conductances

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
    graph = Graph.Erdos_Renyi(400,.1)
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

    #get eigenvalue of v2
    eigv_v2 = get_eigv2(graph,v2)

    #calculate conductance using cheeger's inequality
    v2_c = v2.copy()

    #use D^(1/2) to calculate v2(a) / d(a) for cheeger
    for i in range(len(v2)):
        v2_c[i] = v2_c[i] / (degrees[i]*degrees[i])
    conductances = get_conductances(graph,v2_c)

    #find set of lowest conductance
    min_index = conductances.index(min(conductances))
    min_set = argsort(v2_c)[:min_index+1]

    #output relevant values
    #print "v2: " + str(v2)
    #print "Eigenvalue v2: " + str(eigv_v2)
    #print "Set of lowest conductance: " + str(min_set)
    #print "T value: " + str(min_index + 1)
    #print "Conductance value: " + str(min(conductances))
    #print "(Conductance(S(t))^2 / 4): " + str(min(conductances)**2 / 4.0)
    #print "Mu: " + str(1 - float(eigv_v2[0]))

main()
