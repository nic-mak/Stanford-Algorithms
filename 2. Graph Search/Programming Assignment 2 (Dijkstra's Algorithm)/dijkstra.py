from collections import defaultdict

FILENAME = "dijkstraData.txt"

class Dijkstra:
    def __init__(self):
        self.vertices = set()
        self.vertices_explored = set()
        self.vertices_explored_distance = {}
        self.edge = defaultdict(list)
        self.edge_distance = defaultdict(lambda: 1000000)

    def get_graph(self, filename):
        file = open(filename, "r")

        for row in file.readlines():
            split_row = row.split()  #Each element of list is now 'vertex,weight'. Need to split further
            u = int(split_row[0])

            for vertex_and_weight_str in split_row[1:]:  #[1:] to remove u
                v, weight = vertex_and_weight_str.split(',')
                v, weight = int(v), int(weight)
                self.add_edge(u=u, v=v, weight=weight)
                self.add_vertex(u)
                self.add_vertex(v)

    def add_edge(self, u, v, weight):
        self.edge[u].append(v)
        self.edge_distance[(u, v)] = weight

    def add_vertex(self, vertex):
        self.vertices.add(vertex)

    def get_vertex_shortest_distance(self, vertex):
        return self.vertices_explored_distance[vertex]

    def set_vertex_explored(self, vertex):
        self.vertices_explored.add(vertex)

    def set_vertex_explored_distance(self, vertex, distance):
        self.vertices_explored_distance[vertex] = distance

    def calculate_shortest_distances(self, source_vertex):
        self.set_vertex_explored(source_vertex)
        self.set_vertex_explored_distance(source_vertex, 0)

        while self.vertices != self.vertices_explored:
            edge, distance = self.get_edge_next()
            v, w = edge
            self.set_vertex_explored(w)
            self.set_vertex_explored_distance(vertex=w, distance=distance)

    def get_edge_next(self):
        min_distance = 100000
        min_edge = None

        for edge in self.edge_distance:
            v, w = edge
            if v in self.vertices_explored and w not in self.vertices_explored:
                distance = self.vertices_explored_distance[v] + self.edge_distance[edge]
                if distance < min_distance:
                    min_distance, min_edge = distance, edge

        return min_edge, min_distance

    def get_shortest_distances(self, vertices_list):
        distances_list = []

        for vertex in vertices_list:
            distance = self.get_vertex_shortest_distance(vertex)
            distances_list.append(distance)

        return distances_list


if __name__ == "__main__":
    dijkstra = Dijkstra()
    dijkstra.get_graph(FILENAME)
    dijkstra.calculate_shortest_distances(source_vertex=1)
    distances = dijkstra.get_shortest_distances([7,37,59,82,99,115,133,165,188,197])

    answer = ""
    for distance in distances:
        answer = answer + str(distance) + ","

    print(answer)
