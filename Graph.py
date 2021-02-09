import heapq
import math


class Graph:

    def __init__(self, vertex_count):
        self.adjacency_list = [[] for _ in range(vertex_count)]
        self.vertex_count = vertex_count
        self.edge_count = 0

    # adds edge and returns new edge count
    def add_edge(self, origin, target, weight, base_length):
        self.adjacency_list[origin].append([target, weight, base_length])
        self.adjacency_list[target].append([origin, weight, base_length])
        self.edge_count += 1
        return self.edge_count

    # adds vertex and returns index of  new edge
    def add_vertex(self):
        self.adjacency_list.append([])
        self.vertex_count += 1
        return len(self.adjacency_list) - 1

    def get_weight(self, origin, dest):
        if origin == dest:
            return 0
        for (node, weight, length) in self.adjacency_list[origin]:
            if node == dest:
                return weight, length
        return math.inf

    def set_weight(self, origin, dest, new_weight):
        if origin == dest:
            return
        for i in range(len(self.adjacency_list[origin])):
            (node, weight, length) = self.adjacency_list[origin][i]
            if node == dest:
                self.adjacency_list[origin][i][1] = new_weight
                break
        for i in range(len(self.adjacency_list[dest])):
            (node, weight, length) = self.adjacency_list[dest][i]
            if node == origin:
                self.adjacency_list[dest][i][1] = new_weight
                break

    def adjust_weight_to_traffic(self, origin, dest, TRAFFIC_FACTOR, count):
        if origin == dest:
            return
        for i in range(len(self.adjacency_list[origin])):
            (node, weight, length) = self.adjacency_list[origin][i]
            if node == dest:
                self.adjacency_list[origin][i][1] = length * (1 + TRAFFIC_FACTOR * count)
                break
        for i in range(len(self.adjacency_list[dest])):
            (node, weight, length) = self.adjacency_list[dest][i]
            if node == origin:
                self.adjacency_list[dest][i][1] = length * (1 + TRAFFIC_FACTOR * count)
                break

    # dijkstra function returns two lists in a tuple.
    # first is dist from source,
    # second is previous node to reach node in order to backtrack and find path
    def run_dijkstra(self, source, dest):
        visited = [False] * self.vertex_count
        dist = [math.inf] * self.vertex_count
        prev = [math.inf] * self.vertex_count
        dist[source] = 0

        heapQueue = [(dist[source], source)]
        visited[source] = True
        while len(heapQueue) != 0 and not visited[dest]:
            current = heapq.heappop(heapQueue)
            currentNode = current[1]
            visited[currentNode] = True
            for (neighbour, weight, length) in self.adjacency_list[currentNode]:
                if not visited[neighbour]:
                    new_dist = dist[currentNode] + weight
                    if new_dist < dist[neighbour]:
                        dist[neighbour] = new_dist
                        prev[neighbour] = currentNode
                        heapq.heappush(heapQueue, (dist[neighbour], neighbour))

        return dist, prev


    def get_path(self, origin, dest):
        (dists, prevs) = self.run_dijkstra(origin, dest)
        if dists[dest] == math.inf:
            return None
        path = []
        it = dest
        while it != origin:
            path.append(it)
            it = prevs[it]
        path.append(origin)
        return path[::-1], dists[dest]

    def reset_to_base_weight(self):
        for list in self.adjacency_list:
            for j in range(len(list)):
                list[j][1] = list[j][2]  # set weight to length
