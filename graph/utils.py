import numpy as np
import networkx as nx
import prettytable as pt


def load_self_defined_graph_format(file):
    with open(file, 'r') as f:
        lines = f.readlines()
    graph_type = 0
    nodes = []
    edges = []
    weights = []
    if lines is not None:
        for i, line in enumerate(lines):
            line = str.strip(line)
            if i == 0:
                if len(line) == 0:
                    graph_type = 0  # by default, undirected
                else:
                    graph_type = int(line)
            elif i == 1:
                if len(line) == 0:
                    print('warning: empty node list')
                parts = str.split(line, ',')
                for part in parts:
                    part = str.strip(part)
                    if '|' in part and '-' in part:
                        p = part.split('|')
                        prefix = str.strip(p[0])
                        frto = str.strip(p[1]).split('-')
                        fr = int(frto[0])
                        to = int(frto[1])
                        for cur in range(fr, to + 1):
                            nodes.append(prefix + str(cur))
                    else:
                        nodes.append(part)
            else:
                if len(line) == 0:
                    continue
                parts = str.split(line, ',')
                if len(parts) < 2:
                    raise Exception('bad edge: ' + line)
                node_from = str.strip(parts[0])
                node_to = str.strip(parts[1])
                if node_from not in nodes:
                    raise Exception('unknown node: ' + node_from)
                if node_to not in nodes:
                    raise Exception('unknown node: ' + node_to)
                if len(parts) < 3:
                    weight = 1.0  # weight can be ignored, by default: 1.0
                else:
                    weight = float(str.strip(parts[2]))
                edge = (node_from, node_to)
                edges.append(edge)
                weights.append(weight)

    adj_mat = np.zeros((len(nodes), len(nodes)), dtype=np.float64)
    for k, edge in enumerate(edges):
        i = nodes.index(edge[0])
        j = nodes.index(edge[1])
        w = weights[k]
        adj_mat[i, j] = w
        if graph_type == 0:
            adj_mat[j, i] = w
    return adj_mat, nodes


def use_node(indexes, nodes=None):
    results = []
    for index in indexes:
        if isinstance(index, set):
            index = list(index)
            result = use_node(index, nodes)
            results.append(set(result))
        elif isinstance(index, tuple):
            index = list(index)
            result = use_node(index, nodes)
            results.append(tuple(result))
        elif isinstance(index, list):
            result = use_node(index, nodes)
            results.append(result)
        elif isinstance(index, int) \
                or isinstance(index, np.int16) \
                or isinstance(index, np.int32) \
                or isinstance(index, np.int64):
            if nodes is None:
                result = index + 1
            else:
                result = nodes[index]
            results.append(result)
        else:
            raise Exception('unknown type {}'.format(type(index)))
    return results


def G(adj_mat, nodes=None, directed=False):
    if nodes is not None and len(adj_mat) != len(nodes):
        print('warning: invalid nodes. ignored')
        nodes = None
    if directed:
        g = nx.DiGraph()
    else:
        g = nx.Graph()
    for i in range(len(adj_mat)):
        for j in range(len(adj_mat)):
            if adj_mat[i, j] != 0:
                if nodes is not None:
                    node_i = nodes[i]
                    node_j = nodes[j]
                    g.add_edge(node_i, node_j, weight=adj_mat[i, j])
                else:
                    g.add_edge(i, j, weight=adj_mat[i, j])
    return g


def print_adjacy_matrix(adj_mat, nodes, title=None):
    HIGHLIGHT_STR = "\033[7m{}\033[0m"
    WRONG_STR = "\033[31m{}\033[0m"
    table = pt.PrettyTable()
    if title is not None:
        table.title = title
    field_names = ['']
    field_names.extend(nodes)
    table.field_names = field_names
    n = adj_mat.shape[0]
    for i in range(n):
        row = []
        row.append(nodes[i])
        for j in range(n):
            c = adj_mat[i, j]
            if c > 0:
                row.append(HIGHLIGHT_STR.format(c))
            elif c < 0:
                row.append(WRONG_STR.format(c))
            else:
                row.append(c)
        table.add_row(row)
    print(table)
