from queue import PriorityQueue


def mst_prim(adj_mat, start):
    V = set(range(len(adj_mat)))
    S = {start}
    C = V.difference(S)
    mst_edges = []
    while len(C) > 0:
        q = PriorityQueue()
        for i in S:
            for j in C:
                w = adj_mat[i, j]
                if w > 0:
                    q.put((w, (i, j)))
        j = q.get_nowait()
        S = S.union({j[1][1]})
        C = V.difference(S)
        mst_edges.append(j)
    return mst_edges


if __name__ == '__main__':
    from utils import *

    adj_mat, nodes = load_self_defined_graph_format('input/mst.txt')
    print('# PRIM')
    edges = mst_prim(adj_mat, 0)
    print(use_node([edge[1] for edge in edges], nodes))
    print('weight =', sum([edge[0] for edge in edges]))
