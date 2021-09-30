from collections import defaultdict

GRAPHS = ['g1.txt', 'g2.txt', 'g3.txt']


class ShortestPath:
    def __init__(self):
        self.filename = None
        self.number_nodes = None
        self.number_edges = None
        self.nodes = []
        self.edges = {}

    def get_filename(self):
        return self.filename

    def get_nodes(self):
        return self.nodes

    def get_number_nodes(self):
        return self.number_nodes

    def get_edges(self):
        return self.edges

    def get_number_edges(self):
        return self.number_edges

    def get_data(self):
        file = open(self.filename, "r")
        file_list = file.readlines()

        for i in range(0, len(file_list)):
            if i == 0:
                number_nodes, number_edges = file_list[i].split()
                self.set_number_nodes(int(number_nodes))
                self.set_number_edges(int(number_edges))
            else:
                node_start, node_end, node_length = file_list[i].split()
                node_start, node_end, node_length = int(node_start), int(node_end), int(node_length)
                self.set_edge(node_start, node_end, node_length)
                self.set_node(node_start)
                self.set_node(node_end)
        print('Graph data loaded...')

    def get_edge_cost(self, edge):
        edges = self.get_edges()
        return edges[edge]

    def set_graph(self, filename):
        self.filename = filename

    def set_number_nodes(self, number_nodes):
        self.number_nodes = number_nodes

    def set_number_edges(self, number_edges):
        self.number_edges = number_edges

    def set_node(self, node):
        if node not in self.nodes:
            self.nodes.append(node)
        self.nodes.sort()

    def set_edge(self, node_start, node_end, node_length):
        self.edges[(node_start, node_end)] = node_length

    def all_pairs(self):
        # The Floyd-Warshall Algorithm will be used to calculate all pairs shortest path in a given graph
        print('Starting Floyd-Warshall Algorithm to calculate all pairs shortest path...')

        # Initialising empty 3-dimensional array, indexed by i,j,k
        # i, j represent an arbitrary start and end node
        # k represents subproblem size (P = shortest i, j path where all internal nodes have index < k)
        print('Initialising storage array...')
        number_nodes = self.get_number_nodes()
        n = number_nodes + 1
        array = self.initialise_3d_array()

        # Initialising base cases
        print('Initialising base cases...')
        for i in range(1, number_nodes+1):
            for j in range(1, number_nodes+1):
                edge = (i, j)
                if i == j:
                    # Same node, shortest path = 0
                    array[i][j][0] = 0
                elif self.edge_exists(edge):
                    array[i][j][0] = self.get_edge_cost(edge)
                else:
                    array[i][j][0] = float('inf')

        # Solving subproblems
        print('Solving subproblems...')
        min_uv_distance = float('inf')
        min_edge = None
        for k in range(1, n):
            print(f'Solving subproblem k={k}')
            for i in range(1, n):
                for j in range(1, n):
                    case1 = array[i][j][k-1]
                    case2 = array[i][k][k-1] + array[k][j][k-1]
                    array[i][j][k] = min(case1, case2)

                    if k >= 3:
                        # Subproblems of size k-2 are cleared out to optimise space complexity
                        array[i][j].pop(k-2, None)

                    if k == number_nodes:
                        # Min u,v distance for k=n is cached to be returned later
                        if array[i][j][k] < min_uv_distance:
                            min_uv_distance = array[i][j][k]
                            min_edge = (i, j)

        # Checking for negative cost cycles
        for i in range(1, n):
            if array[i][i][number_nodes] < 0:
                print(f"Graph {self.get_filename()} contains negative cost cycle(s)")
                return

        print(f"Graph {self.get_filename()} does not contain negative cost cycle(s)")
        print(f'The minimum d(u,v) is {min_uv_distance}')
        print(f'This corresponds to edge {min_edge}')
        return min_uv_distance

    def initialise_3d_array(self):
        # array = {a: {b: {c: 0 for c in range(0, n+1)} for b in range(0, n+1)} for a in range(0, n+1)}
        array = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: float('inf'))))
        return array

    def edge_exists(self, edge):
        edges = self.get_edges()
        return edge in edges


if __name__ == '__main__':
    sp = ShortestPath()
    sp.set_graph(GRAPHS[2])
    sp.get_data()
    sp.all_pairs()

    print("Graph g1.txt contains negative cost cycle(s)")
    print("Graph g2.txt contains negative cost cycle(s)")
    print("Graph g3.txt does not contain negative cost cycle(s)")
    print("The minimum d(u,v) is -19")
    print("This corresponds to edge (399, 904)")
