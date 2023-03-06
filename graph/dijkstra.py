from queue import PriorityQueue



def get_path(prev, start, end):
    path = []
    node = end
    while node != start:
        path.append(node)
        node = prev[node]
    path.append(start)
    path.reverse()
    return path


def dijkstra(adj_mat, start):
    V = set(range(len(adj_mat)))
    S = {start}
    dist = [float('inf')] * len(V)
    dist[start] = 0
    C = V.difference(S)
    prev = dict()
    for i in C:
        w = adj_mat[start, i]
        if w > 0:
            if dist[i] > w:
                dist[i] = w
                prev[i] = start
    while len(C) > 0:
        q = PriorityQueue()
        for j in C:
            d = dist[j]
            q.put((d, j))
        j = q.get_nowait()
        S = S.union({j[1]})
        C = V.difference(S)
        for i in C:
            w = adj_mat[j[1], i]
            if w > 0:
                if dist[i] > dist[j[1]] + w:
                    dist[i] = dist[j[1]] + w
                    prev[i] = j[1]
    results = []
    for i in range(len(V)):
        result = []
        result.append(dist[i])
        result.append(get_path(prev, 0, i))
        results.append(result)
    return results


if __name__ == '__main__':
    from utils import *
    adj_mat, nodes = load_self_defined_graph_format('input/dijkstra.txt')
    print_adjacy_matrix(adj_mat, nodes)
    results = dijkstra(adj_mat, 0)
    for result in results:
        print(result[0], end=' = ')
        print(use_node(result[1], nodes))
