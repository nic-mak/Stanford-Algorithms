import math

DATA = 'clustering1.txt'


class GreedyCluster:
    def __init__(self):
        self.number_nodes = 0
        self.edge_costs = {}
        self.clusters = {}
        self.leaders = {}

    def get_number_nodes(self):
        return self.number_nodes

    def get_edge_costs(self):
        return self.edge_costs

    def get_nodes_from_edge(self, edge):
        return edge[0], edge[1]

    def get_clusters(self):
        return self.clusters

    def get_node_leader(self, node):
        return self.leaders[node]

    def get_data(self, filename):
        file = open(filename, "r")
        file_list = file.readlines()

        edge_costs = {}
        clusters = {}

        for i in range(0, len(file_list)):
            if i == 0:
                number_nodes = file_list[i]
                self.set_number_nodes(int(number_nodes))

            else:
                node_1, node_2, cost = file_list[i].split()
                node_1, node_2 = int(node_1), int(node_2)
                edge = (node_1, node_2)
                edge_costs[edge] = int(cost)

                clusters[node_1] = [node_1]
                clusters[node_2] = [node_2]
                self.set_node_leader(node_1, node_1)
                self.set_node_leader(node_2, node_2)

        self.set_edge_costs(edge_costs)
        self.set_clusters(clusters)

    def set_number_nodes(self, number):
        self.number_nodes = number

    def set_edge_costs(self, edge_costs):
        self.edge_costs = edge_costs

    def set_clusters(self, clusters):
        self.clusters = clusters

    def set_node_leader(self, node, leader):
        self.leaders[node] = leader

    def get_closest_nodes(self, return_edge_cost=False):
        edge_costs = self.get_edge_costs()

        min_edge = None
        min_edge_cost = math.inf

        for edge in edge_costs:
            edge_cost = edge_costs[edge]
            node_1, node_2 = self.get_nodes_from_edge(edge)
            leader_node_1, leader_node_2 = self.get_node_leader(node_1), self.get_node_leader(node_2)

            if leader_node_1 != leader_node_2:
                if edge_cost < min_edge_cost:
                    min_edge = edge
                    min_edge_cost = edge_cost

        p, q = self.get_nodes_from_edge(min_edge)

        if return_edge_cost:
            return p, q, min_edge_cost
        return p,q

    def merge_clusters(self, node_1, node_2):
        p, q = self.get_node_leader(node_1), self.get_node_leader(node_2)

        clusters = self.get_clusters()

        cluster_p, cluster_q = clusters[p], clusters[q]
        cluster_size_p, cluster_size_q = len(cluster_p), len(cluster_q)

        if cluster_size_p >= cluster_size_q:
            new_leader, subsumed_leader = p, q
            new_leader_cluster = cluster_p
            subsumed_cluster = cluster_q

        elif cluster_size_p < cluster_size_q:
            new_leader, subsumed_leader = q, p
            new_leader_cluster = cluster_q
            subsumed_cluster = cluster_p

        for node in subsumed_cluster:
            self.set_node_leader(node=node, leader=new_leader)
        new_leader_cluster.extend(subsumed_cluster)

        clusters[new_leader] = new_leader_cluster
        del clusters[subsumed_leader]
        self.set_clusters(clusters)

    def cluster(self, k):
        number_clusters = self.get_number_nodes()

        while number_clusters != k:
            node_1, node_2 = self.get_closest_nodes()
            self.merge_clusters(node_1, node_2)
            number_clusters -= 1

    def get_maximum_spacing(self):
        p, q, min_edge_cost = self.get_closest_nodes(return_edge_cost=True)
        return min_edge_cost


if __name__ == "__main__":
    greedy = GreedyCluster()
    greedy.get_data(DATA)
    greedy.cluster(k=4)
    maximum_spacing = greedy.get_maximum_spacing()
    print(maximum_spacing)
