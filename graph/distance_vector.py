from utils import *
import networkx as nx
import prettytable as pt

def get_path_weight(path, adj_mat):
    weight = 0
    edges = []
    for i in range(len(path)-1):
        edges.append((path[i], path[i+1]))
    for edge in edges:
        weight += adj_mat[edge[0]][edge[1]]
    return weight


def direct_distance(adj_mat, node):
    dist_tab = dict()
    neighbors = [i for i, v in enumerate(adj_mat[node]) if v != 0]
    for i in range(len(adj_mat)):
        if i != node:
            for j in neighbors:
                # key = (目标，途径邻居）
                dist_tab[(i, j)] = float('inf') if i != j else adj_mat[node][j]
    return dist_tab

def distance_tables(adj_mat):

    g = G(adj_mat)

    dist_tables = dict()
    for node in range(len(adj_mat)):
        dist_tables[node] = direct_distance(adj_mat, node)

    for source in dist_tables:
        dist_table = dist_tables[source]
        for key, value in dist_table.items():
            if value == float('inf'):
                destination = key[0]
                neighbor = key[1]

                paths1 = nx.all_simple_paths(g, source, neighbor)
                paths1 = [path for path in paths1]
                paths2 = nx.all_simple_paths(g, neighbor, destination)
                paths2 = [path for path in paths2]
                paths = []
                for path1 in paths1:
                    for path2 in paths2:
                        path = []
                        path.extend(path1)
                        path.extend(path2[1:])
                        paths.append(path)
                if source != destination:
                    dpaths = nx.all_simple_paths(g, source, destination)
                    for path in dpaths:
                        paths.append(path)

                paths = [path for path in paths if path[1] == neighbor]  # 从邻居出发！
                weights = [get_path_weight(path, adj_mat) for path in paths]
                if len(weights) > 0:
                    min_weight = min(weights)
                    path = paths[weights.index(min_weight)]
                    dist_table[key] = (min_weight, path)

    return dist_tables


def print_dist_table(source, dist_table, nodes):
    table = pt.PrettyTable()
    table.title = f'Distance Table of {nodes[source]}'
    field_names = [f'DST^{nodes[source]}()']
    neighbors = list(set([key[1] for key in dist_table.keys()]))
    field_names.extend(use_node(neighbors, nodes))
    table.field_names = field_names
    destinations = set([key[0] for key in dist_table.keys()])
    for destination in destinations:
        row = [nodes[destination]]
        for neighbor in neighbors:
            value = dist_table[(destination, neighbor)]
            if type(value) is tuple:
                row.append(f'{value[0]} - {use_node(value[1], nodes)}')
            else:
                row.append(value)
        table.add_row(row)
    print(table)



if __name__ == '__main__':

    adj_mat, nodes = load_self_defined_graph_format('input/distance_vector.txt')
    dist_tables = distance_tables(adj_mat)

    for source in dist_tables:
        print_dist_table(source, dist_tables[source], nodes)
        print()








