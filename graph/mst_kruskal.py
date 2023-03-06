from queue import PriorityQueue


def mst_kruskal(adj_mat, k=1):
    n = len(adj_mat)
    p = PriorityQueue()
    for i in range(n):
        for j in range(i + 1, n):
            w = adj_mat[i, j]
            if w > 0:
                p.put_nowait((w, (i, j)))

    new_mark = n
    marks = list(range(n))
    mst_edges = []

    while len(mst_edges) < n - k:
        edge = p.get_nowait()
        u_mark = marks[edge[1][0]]
        v_mark = marks[edge[1][1]]
        if u_mark != v_mark:
            new_mark += 1
            for i in range(len(marks)):
                if marks[i] == u_mark or marks[i] == v_mark:
                    marks[i] = new_mark
            mst_edges.append(edge)

    if k > 1:
        clusters = dict()
        for i, mark in enumerate(marks):
            if mark not in clusters:
                clusters[mark] = set([])
            cluster = clusters[mark]
            cluster.add(i)
        return list(clusters.values())
    else:
        return mst_edges


if __name__ == '__main__':
    from utils import *

    adj_mat, nodes = load_self_defined_graph_format('input/mst.txt')
    print('# KRUSKAL')
    edges = mst_kruskal(adj_mat)
    print(use_node([edge[1] for edge in edges], nodes))
    print('weight =', sum([edge[0] for edge in edges]))
