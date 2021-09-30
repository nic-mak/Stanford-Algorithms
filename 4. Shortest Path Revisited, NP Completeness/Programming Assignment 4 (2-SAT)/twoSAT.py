from kosaraju import Graph
import threading
import sys


FILENAMES = ["2sat1.txt", "2sat2.txt", "2sat3.txt", "2sat4.txt", "2sat5.txt", "2sat6.txt"]


class TwoSAT:
    def __init__(self):
        self.graph = None
        self.number_clauses = 0
        self.clauses = []

    def clear_data(self):
        self.graph = None
        self.number_clauses = 0
        self.clauses = []

    def get_number_clauses(self):
        return self.number_clauses

    def get_data(self, filename):
        self.clear_data()

        file = open(filename, "r")
        file_list = file.readlines()

        clauses = []
        for i in range(0, len(file_list)):
            if i == 0:
                self.number_clauses = int(file_list[i])
            else:
                x, y = file_list[i].split()
                x, y = int(x), int(y)
                clauses.append((x, y))

        self.clauses = clauses
        return clauses

    def get_clauses(self):
        return self.clauses

    def clauses_to_graph(self, clauses):
        number_edges = 2 * self.get_number_clauses()
        graph = Graph(number_edges)

        for clause in clauses:
            u, v = clause
            graph.add_edge(-u, v)
            graph.add_edge(-v, u)

        self.graph = graph
        return graph

    def is_satisfiable(self, filename):
        self.get_data(filename)
        clauses = self.get_clauses()
        graph = self.clauses_to_graph(clauses)

        scc_list = graph.kosaraju()

        for scc in scc_list:
            for vertex in scc:
                if -vertex in scc:
                    return False
        return True


if __name__ == "__main__":
    twosat = TwoSAT()

    answer = ""
    for filename in FILENAMES:
        satisfiability = twosat.is_satisfiable(filename)
        if satisfiability is True:
            answer += "1"
        else:
            answer += "0"
    print(answer)
