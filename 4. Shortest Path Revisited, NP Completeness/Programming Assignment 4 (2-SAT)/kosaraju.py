from collections import defaultdict
import threading
import sys


FILENAME = "2sat1.txt"

GENERATING_T = "generating t"
GENERATING_SCC = "generating scc"


class Graph:

    def __init__(self, vertices):
        self.number_of_vertices = vertices
        self.edges = defaultdict(list)
        self.vertices_explored = defaultdict(lambda: False)
        self.finishing_times = {}  #key:value = finishing_time:vertex
        self.current_t = 0
        self.recent_vertex = None
        self.current_scc = []

    def get_graph_edges(self):
        return self.edges

    def get_vertex_connected(self, vertex):
        return self.edges[vertex]

    def get_graph(self, filename):
        file = open(filename, "r")

        for row in file.readlines():
            split_row_str = row.split()
            split_row_int = list(map(lambda x: int(x), split_row_str))

            u, v= split_row_int[0], split_row_int[1]
            self.add_edge(u, v)

    def get_graph_reverse(self):
        graph_edges = self.get_graph_edges()
        new_graph = Graph(self.number_of_vertices)

        for i in graph_edges:
            for j in graph_edges[i]:
                new_graph.add_edge(j, i)

        return new_graph

    def get_vertex_explored(self, vertex):
        return self.vertices_explored[vertex]

    def get_recent_vertex(self):
        return self.recent_vertex

    def get_graph_length(self):
        return self.number_of_vertices

    def set_vertex_explored(self, vertex):
        self.vertices_explored[vertex] = True

    def set_vertex_finishing_time(self, vertex):
        self.finishing_times[self.current_t] = vertex

    def set_recent_vertex(self, vertex):
        self.recent_vertex = vertex

    def add_edge(self, u, v):
        self.edges[u].append(v)

    def dfs(self, vertex):

        self.set_vertex_explored(vertex)
        #self.set_vertex_leader(vertex=vertex, leader=self.get_recent_vertex())

        vertex_edges = self.get_vertex_connected(vertex)
        for j in vertex_edges:
            if self.get_vertex_explored(j) is False:
                self.dfs(j)

        self.current_t += 1
        self.set_vertex_finishing_time(vertex)


    def dfs_loop(self):
        n = self.get_graph_length()
        i = n

        while i >= 1:
            if self.get_vertex_explored(i) is False:
                self.set_recent_vertex(i)
                self.dfs(i)

            i -= 1

    def dfs_generate_scc(self, vertex):
        self.set_vertex_explored(vertex)

        vertex_edges = self.get_vertex_connected(vertex)
        for j in vertex_edges:
            if self.get_vertex_explored(j) is False:
                self.dfs_generate_scc(j)
                self.current_scc.append(j)

    def kosaraju(self):
        graph_reversed = self.get_graph_reverse()
        graph_reversed.dfs_loop()
        finishing_time_dict = graph_reversed.finishing_times

        self.vertices_explored = defaultdict(lambda: False)
        i = len(finishing_time_dict)
        scc_list = []

        while i >= 1:
            self.current_scc = []
            vertex = finishing_time_dict[i]
            if self.vertices_explored[vertex] is False:
                self.current_scc.append(vertex)
                self.dfs_generate_scc(vertex)
                scc = self.current_scc
                scc_list.append(scc)
            i -= 1

        return scc_list

    def find_biggest_sccs(self, n=5):
        scc_list = self.kosaraju()
        scc_size_list = []

        for scc in scc_list:
            scc_size = len(scc)
            scc_size_list.append(scc_size)

        scc_size_list.sort(reverse=True)

        print(scc_size_list[0:n])
        return scc_size_list[0:n]


if __name__ == "__main__":
    graph = Graph(875714)
    graph.get_graph(FILENAME)
    threading.stack_size(67108864)
    sys.setrecursionlimit(2**20)
    thread = threading.Thread(target=graph.find_biggest_sccs)
    thread.start()
