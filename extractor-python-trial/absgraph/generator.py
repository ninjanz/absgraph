from absgraph.utils.converter import convert
from itertools import permutations
from random import sample
from scipy.spatial.distance import canberra, cosine

import graphsim as gs
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st

import collections
import math


def produce_nodes(graph_obj, params):
    _nodes = []
    for i in range(params['n_nodes']):
        _nodes.append('A' + str(i))

    graph_obj.add_nodes_from(_nodes)


def produce_random_edges(graph_obj, params):
    # create possible edges randomly
    cycles_bool = check_number_cycles(params)
    possible_edges = permutations(graph_obj.nodes(), 2)

    if cycles_bool and params['n_cycles'] > 0:
        sample_size = params['n_edges'] - params['n_cycles']
    else:
        sample_size = params['n_edges']

    chosen_edges = sample(list(possible_edges), sample_size)

    # add the edges
    graph_obj.add_edges_from(chosen_edges)

    # add cycles
    if cycles_bool and params['n_cycles'] > 0:
        cycles = [(t[1], t[0]) for t in sample(chosen_edges, params['n_cycles'])]
        graph_obj.add_edges_from(cycles)


def calculate_edges(params):
    return math.ceil(params['density'] * params['n_nodes'] *
                     (params['n_nodes'] - 1))


def check_number_cycles(params):
    params['n_edges'] = calculate_edges(params)
    non_cycle_edges = params['n_edges'] - params['n_cycles']

    if params['n_cycles'] > non_cycle_edges:
        print('\nError: Not possible to draw cycles with this density, will proceed without cycles')
        return False

    else:
        return True


def generate_random(params):
    g = nx.DiGraph()

    produce_nodes(g, params)
    produce_random_edges(g, params)

    return g


def simrank_sim(g1, g2):
    gsim1 = gs.simrank(g1)
    gsim2 = gs.simrank(g2)

    scores = collections.defaultdict(list)

    for x, y in zip(gsim1, gsim2):
        scores['cosine'].append(1-cosine(x, y))
        scores['canberra'].append(canberra(x, y))

    print('\n----------Similarity Scores----------\n')
    for k, v in scores.items():
        score = sum(v) / len(v)
        print(k + ': ' + str(score))
    print('\n-----------------End-----------------\n')


def partial_gfpc(g):
    # 1 eigenvector centrality value

    vertex_features = [
        list(nx.eigenvector_centrality(g, max_iter=500).values()),
        list(nx.pagerank(g).values()),
        list(nx.average_neighbor_degree(g).values())
    ]

    maximum_degree = 0
    degrees = []
    in_deg = []
    out_deg = []
    for v_in, v_out in zip(g.in_degree().values(), g.out_degree().values()):
        total_degree = v_in + v_out
        in_deg.append(v_in)
        out_deg.append(v_out)
        degrees.append(total_degree)

        if total_degree > maximum_degree:
            maximum_degree = total_degree

    vertex_features.append(degrees)
    vertex_features.append(in_deg)
    vertex_features.append(out_deg)

    return vertex_features, maximum_degree


def fvec_decompose(vf):
    decomposed_vec = []

    for feature in vf:
        decomposed_vec.append(np.mean(feature))
        decomposed_vec.append(np.std(feature))
        decomposed_vec.append(np.var(feature))
        decomposed_vec.append(st.skew(feature))
        decomposed_vec.append(st.kurtosis(feature))
        decomposed_vec.append(max(feature))
        decomposed_vec.append(min(feature))

    return decomposed_vec