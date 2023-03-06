from utils import *


def get_path_weight(path, adj_mat):
    weight = 0
    edges = []
    for i in range(len(path) - 1):
        edges.append((path[i], path[i + 1]))
    for edge in edges:
        weight += adj_mat[edge[0]][edge[1]]
    return weight


def bellman_ford(adj_mat, nodes, end):
    g = G(adj_mat, directed=True)
    n = len(adj_mat)
    M = [[None for _ in range(n)] for _ in range(n)]
    for i in range(n):
        if i != end:
            M[0][i] = float('inf')
        else:
            M[0][i] = 0
    for i in range(1, n):
        for x in range(n):
            M[i][x] = M[i - 1][x]
        for v in range(n):
            v1 = M[i][v]
            paths = nx.all_simple_paths(g, v, end)
            paths = [path for path in paths if len(path) == i + 1]
            [print(f'use {i} edges: {nodes[v]}->{nodes[end]}', use_node(path, nodes), 'weight =',
                   get_path_weight(path, adj_mat)) for path in paths]
            v2 = float('inf')
            if len(paths) > 0:
                min_weight_path = None
                min_weight = float('inf')
                if len(paths) > 0:
                    for path in paths:
                        pw = get_path_weight(path, adj_mat)
                        if min_weight > pw:
                            min_weight_path = path
                            min_weight = pw
                w = min_weight_path[1]
                v2 = M[i - 1][w] + adj_mat[v][w]
            M[i][v] = min(v1, v2)
    return M


def print_bellman_ford(M, nodes):
    table = pt.PrettyTable()
    table.title = 'Bellman Ford'
    field_names = ['# of Edges']
    field_names.extend(nodes)
    table.field_names = field_names
    for i in range(1, len(M)):
        row = [i]
        row.extend(M[i])
        table.add_row(row)
    print(table)


if __name__ == '__main__':
    adj_mat, nodes = load_self_defined_graph_format('input/bellman_ford.txt')
    g = G(adj_mat, nodes, directed=True)

    M = bellman_ford(adj_mat, nodes, len(adj_mat) - 1)
    print_bellman_ford(M, nodes)
