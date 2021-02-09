from math import sqrt
from Graph import *

Traffic_Factor = 0.3
id_data_dict = {}  # dict[id]=(x, y, index_in_graph)
response_traffic_list = []  # members are (start, end, [path]) path is using graph indices , not ids
graph = Graph(0)


def calculate_weight(length, traffic):
    return length * (1 + traffic * Traffic_Factor)


def calculate_length(vector1, vector2):
    return sqrt((vector1[0] - vector2[0]) ** 2 + (vector1[1] - vector2[1]) ** 2)


# updates weights to use in input time
def update_weights(time):
    traffic_count = {}
    for i in range(len(response_traffic_list)):
        if response_traffic_list[i][0] < time < response_traffic_list[i][1]:
            path = response_traffic_list[i][2]
            for j in range(len(path) - 1):
                if (path[j], path[j + 1]) in traffic_count:
                    traffic_count[(path[j], path[j + 1])] += 1
                else:
                    traffic_count[(path[j], path[j + 1])] = 1
    for edge in traffic_count.keys():
        graph.adjust_weight_to_traffic(edge[0], edge[1], Traffic_Factor, traffic_count[edge])


def add_response(request_time, drive_time, response_path):
    response_traffic_list.append((request_time, request_time + drive_time, response_path))


def read_file(filename):
    global graph, id_data_dict
    f = open(filename, "r")
    [n, m] = map(int, f.readline().split())
    for i in range(n):
        (node_id, x, y) = map(float, f.readline().split())
        node_id = int(node_id)
        index = graph.add_vertex()
        id_data_dict[node_id] = (x, y, index)
    for i in range(m):
        [origin, dest] = map(int, f.readline().split())
        length = calculate_length((id_data_dict[origin][0], id_data_dict[origin][1]),
                                  (id_data_dict[dest][0], id_data_dict[dest][1]))
        graph.add_edge(id_data_dict[origin][2], id_data_dict[dest][2], calculate_weight(length, 0), length)
    f.close()


read_file("m4.txt")
while True:
    graph.reset_to_base_weight()

    (time, origin, dest) = map(float, input().split())
    update_weights(time)
    (path, dist) = graph.get_path(id_data_dict[origin][2], id_data_dict[dest][2])
    drive_time = dist * 120
    add_response(time, drive_time, path)
    for i in path:
        for j in id_data_dict.keys():  # find id for index
            if id_data_dict[j][2] == i:
                print(j, end=" ")
    print()
    print(drive_time)
    print()
