import math

DATA = 'edges.txt'


class Prim:
    def __init__(self, filename):
        self.filename = filename
        self.number_nodes = 0
        self.number_edges = 0
        self.edge_costs = {}
        self.all_nodes = set()

    def get_filename(self):
        return self.filename

    def get_number_nodes(self):
        return self.number_nodes

    def get_edge_costs(self):
        return self.edge_costs

    def get_edge_cost(self, edge):
        edge_costs = self.get_edge_costs()
        return edge_costs[edge]

    def get_all_nodes(self):
        return self.all_nodes

    def get_node_start(self, edge):
        return edge[0]

    def get_node_end(self, edge):
        return edge[1]

    def get_data(self):
        file = open(self.get_filename(), "r")
        file_list = file.readlines()

        edge_costs = {}
        for i in range(0, len(file_list)):
            if i == 0:
                number_nodes, number_edges = file_list[i].split()
                self.set_number_nodes(int(number_nodes))
                self.set_number_edges(int(number_edges))

            else:
                node_1, node_2, cost = file_list[i].split()
                edge = (int(node_1), int(node_2))
                edge_costs[edge] = int(cost)
                self.set_node(int(node_1))
                self.set_node(int(node_2))

        self.set_edge_costs(edge_costs)

    def set_number_nodes(self, number):
        self.number_nodes = number

    def set_number_edges(self, number):
        self.number_edges = number

    def set_edge_costs(self, edge_costs):
        self.edge_costs = edge_costs

    def set_node(self, node):
        self.all_nodes.add(node)

    def get_mst(self):
        all_nodes = self.get_all_nodes()

        spanned_nodes = {2}

        mst = []
        mst_cost = 0

        while spanned_nodes != all_nodes:
            min_edge, min_edge_cost = self.get_cheapest_edge(spanned_nodes=spanned_nodes, current_mst=mst)
            mst.append(min_edge)

            node_end = self.get_node_end(min_edge)
            spanned_nodes.add(node_end)

            mst_cost += min_edge_cost
        return mst, mst_cost

    def get_cheapest_edge(self, spanned_nodes, current_mst):
        edge_costs = self.get_edge_costs()

        min_edge = (0, 0)
        min_edge_cost = math.inf

        for edge in edge_costs:
            node_start = self.get_node_start(edge)
            node_end = self.get_node_end(edge)
            edge_cost = self.get_edge_cost(edge)

            if edge not in current_mst:
                if (node_start in spanned_nodes and node_end not in spanned_nodes):
                    if edge_cost < min_edge_cost:
                        min_edge = (node_start, node_end)
                        min_edge_cost = edge_cost

                elif node_end in spanned_nodes and node_start not in spanned_nodes:
                    if edge_cost < min_edge_cost:
                        min_edge = (node_end, node_start)
                        min_edge_cost = edge_cost

        return min_edge, min_edge_cost


prim = Prim(DATA)
prim.get_data()
mst, mst_cost = prim.get_mst()
print(mst_cost)
