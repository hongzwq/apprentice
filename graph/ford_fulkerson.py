import random
import math
import numpy as np
import networkx as nx


def augment_path(path, flow, residual):
    edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]  # convert path into edges
    b = min([residual[edge[0], edge[1]] for edge in edges])  # find bottleneck edge value
    for edge in edges:  # augment the path with the bottleneck value
        flow[edge[0], edge[1]] += b
    return flow


def get_residual(capacity, flow, **kwargs):  # computer the residual based on capacity and flow
    residual = capacity - flow  # remove the flow from capacity
    residual = residual + flow.T  # add reversed edges
    return residual


def get_path(residual, start, end, **kwargs):
    g = nx.from_numpy_array(residual, create_using=nx.DiGraph)  # build the graph for finding the path
    paths = nx.all_simple_paths(g, start, end)  # find the path from start to end
    paths = [path for path in paths]  # make the path-generator as list
    if len(paths) > 0:  # if we find any path
        return random.choice(paths)  # just choose one randomly
    else:
        return None  # no path found


def ford_fulkerson(adj_mat, start, end, func_path=None, **kwargs):
    if func_path is None:
        func_path = get_path
    capacity = adj_mat  # the adjacy_matrix is the capacity matrix
    flow = np.zeros(np.shape(capacity))  # the flow is initialized as zeros (0)
    residual = get_residual(capacity, flow, **kwargs)  # computer the residual based on flow and capacity
    path = func_path(residual, start, end, **kwargs)  # get a possible path from residual
    while path is not None:  # if the path exists
        flow = augment_path(path, flow, residual)  # augment the path
        residual = get_residual(capacity, flow, **kwargs)  # recompute the residual based on new flow and capacity
        path = func_path(residual, start, end, **kwargs)  # get another path
    # NOTICE: after loop, there are some values for the reversed direction edges
    # need combine the reversed edges with the normal edges
    # e.g. in flow, edge (u,v) = 8, however (v, u) also in flow with value 2
    # need combine it as (u,v) = 8 - 2 = 6
    flow = flow - flow.T
    # after the above combination, will create negative values in flow matrix for edges without reversed edges,
    # just remove them
    flow[flow < 0] = 0
    return flow


def get_residual_delta(capacity, flow, delta):
    residual = capacity - flow  # remove the flow from capacity
    residual = residual + flow.T  # add reversed edges
    residual[residual < delta] = 0  # remove the edges lower than delta
    return residual


def ford_fulkerson_delta(adj_mat, start, end, func_path=None, **kwargs):
    if func_path is None:
        func_path = get_path
    capacity = adj_mat  # the adjacy_matrix is the capacity matrix
    max_idx = np.argmax(capacity, axis=None)
    max_idx = np.unravel_index(max_idx, capacity.shape)
    C = capacity[max_idx]
    delta = 2 ** int(math.ceil(math.log2(C)))
    flow = np.zeros(np.shape(capacity))  # the flow is initialized as zeros (0)
    while delta >= 1:
        residual = get_residual_delta(capacity, flow, delta)  # computer the residual based on flow and capacity
        path = func_path(residual, start, end, **kwargs)  # get a possible path from residual
        while path is not None:  # if the path exists
            flow = augment_path(path, flow, residual)  # augment the path
            residual = get_residual_delta(capacity, flow,
                                          delta)  # recompute the residual based on new flow and capacity
            path = func_path(residual, start, end, **kwargs)  # get another path
        delta /= 2
    flow = flow - flow.T
    flow[flow < 0] = 0
    return flow


def get_least_edges_path(residual, start, end, **kwargs):
    g = nx.from_numpy_array(residual, create_using=nx.DiGraph)  # build the graph for finding the path
    paths = nx.all_simple_paths(g, start, end)  # find the path from start to end
    paths = [path for path in paths]  # make the path-generator as list
    if len(paths) > 0:  # if we find any path
        # find the most quick way ( fewer edges )
        idx = np.argmin([len(path) for path in paths])
        return paths[idx]
    else:
        return None  # no path found


def get_max_bottle_path(residual, start, end, **kwargs):
    g = nx.from_numpy_array(residual, create_using=nx.DiGraph)  # build the graph for finding the path
    paths = nx.all_simple_paths(g, start, end)  # find the path from start to end
    paths = [path for path in paths]  # make the path-generator as list
    max_b = 0
    max_b_path = None
    for path in paths:
        edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]  # convert path into edges
        b = min([residual[edge[0], edge[1]] for edge in edges])  # find bottleneck edge value
        if b > max_b:
            max_b = b
            max_b_path = path
    return max_b_path


if __name__ == '__main__':
    from utils import *

    adj_mat, nodes = load_self_defined_graph_format('input/ford_fulkerson.txt')
    s = nodes.index('s')
    t = nodes.index('t')

    flow = ford_fulkerson(adj_mat, s, t)
    print_adjacy_matrix(flow, nodes, 'Default Ford Fulkerson')

    flow = ford_fulkerson(adj_mat, s, t, func_path=get_least_edges_path)
    print_adjacy_matrix(flow, nodes, 'Least Edges Ford Fulkerson')

    flow = ford_fulkerson(adj_mat, s, t, func_path=get_max_bottle_path)
    print_adjacy_matrix(flow, nodes, 'Max Bottle Ford Fulkerson')

    flow = ford_fulkerson_delta(adj_mat, s, t)
    print_adjacy_matrix(flow, nodes, 'Default Delta Ford Fulkerson')

    flow = ford_fulkerson_delta(adj_mat, s, t, func_path=get_least_edges_path)
    print_adjacy_matrix(flow, nodes, 'Least Edges Delta Ford Fulkerson')

    flow = ford_fulkerson_delta(adj_mat, s, t, func_path=get_max_bottle_path)
    print_adjacy_matrix(flow, nodes, 'Max Bottle Delta Ford Fulkerson')
