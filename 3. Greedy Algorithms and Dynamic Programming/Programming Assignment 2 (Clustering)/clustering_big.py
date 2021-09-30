

DATA = "clustering big.txt"
MINIMUM_DISTANCE = 3


class BigGreedyCluster:
    def __init__(self):
        self.number_nodes = 0
        self.number_bits = 0
        self.index_to_bits = {}
        self.bits_to_index = {}
        self.clusters = {}
        self.leaders = {}

    def get_number_nodes(self):
        return self.number_nodes

    def get_distance(self, node_index_1, node_index_2):
        node_bits_1 = self.get_node_bits(node_index_1)
        node_bits_2 = self.get_node_bits(node_index_2)

        count = 0
        for i in range(len(node_bits_1)):
            if node_bits_1[i] != node_bits_2[i]:
                count += 1
        return count

    def get_node_bits(self, node_index):
        return self.index_to_bits[node_index]

    def get_node_index(self, node_bits):
        return self.bits_to_index[tuple(node_bits)]

    def get_node_leader(self, node_index):
        return self.leaders[node_index]

    def get_clusters(self):
        return self.clusters

    def get_data(self, filename):
        file = open(filename, "r")
        file_list = file.readlines()

        clusters = {}

        for i in range(0, len(file_list)):
            if i == 0:
                number_nodes, number_bits = file_list[i].split()
                self.set_number_nodes(int(number_nodes))
                self.number_bits = int(number_bits)

            else:
                node_bits = list(file_list[i].split())
                if not self.node_exists(node_bits):
                    node_index = len(self.bits_to_index) + 1
                    self.set_node(node_index, node_bits)
                    clusters[node_index] = [node_index]
                    self.leaders[node_index] = node_index

        self.set_number_nodes(len(self.bits_to_index))
        self.set_clusters(clusters)

    def node_exists(self, node_bits):
        node_bits = tuple(node_bits)
        if node_bits in self.bits_to_index:
            return True
        return False

    def set_number_nodes(self, number):
        self.number_nodes = number

    def set_node(self, node_index, node_bits):
        self.index_to_bits[node_index] = node_bits
        self.bits_to_index[tuple(node_bits)] = node_index

    def set_node_leader(self, node_index, leader_index):
        self.leaders[node_index] = leader_index

    def set_clusters(self, clusters):
        self.clusters = clusters

    def get_closest_nodes(self, node_index, distance):
        node_bits = self.get_node_bits(node_index)
        closest_nodes = set()

        if distance == 1:
            for i in range(0, len(node_bits)):
                new_node_bits = node_bits.copy()
                new_node_bits[i] = self.invert_node_bit(new_node_bits[i])

                try:
                    new_node_index = self.get_node_index(new_node_bits)
                except KeyError:
                    continue
                else:
                    closest_nodes.add(new_node_index)

        elif distance == 2:
            for i in range(0, len(node_bits)):
                new_node_bits = node_bits.copy()
                new_node_bits[i] = self.invert_node_bit(new_node_bits[i])
                for j in range(0, len(node_bits)):
                    if i != j:
                        new_new_node_bits = new_node_bits.copy()
                        new_new_node_bits[j] = self.invert_node_bit(new_new_node_bits[j])

                        try:
                            new_node_index = self.get_node_index(new_new_node_bits)
                        except KeyError:
                            continue
                        else:
                            closest_nodes.add(new_node_index)
        return closest_nodes

    def invert_node_bit(self, node_bit):
        if node_bit == '0':
            return '1'
        elif node_bit == '1':
            return '0'

    def merge_clusters(self, node_1, node_2):
        p, q = self.get_node_leader(node_1), self.get_node_leader(node_2)

        if p == q: #Same connected component
            return

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
            self.set_node_leader(node_index=node, leader_index=new_leader)

        new_leader_cluster.extend(subsumed_cluster)

        clusters[new_leader] = new_leader_cluster

        del clusters[subsumed_leader]
        self.set_clusters(clusters)

    def cluster(self):
        number_nodes = self.get_number_nodes()

        for i in range(1, MINIMUM_DISTANCE):
            edges = set()

            print(f"Finding all edges with distance = {i}...")
            for j in range(1, number_nodes):
                closest_nodes = self.get_closest_nodes(j, distance=i)
                for node in closest_nodes:
                    if (node, j) not in edges:
                        edges.add((j, node))

            print(f"Merging edges with distance = {i}...")
            for edge in edges:
                node_1, node_2 = edge
                self.merge_clusters(node_1, node_2)

        clusters = self.get_clusters()
        print(len(clusters))
        return len(clusters)


if __name__ == "__main__":
    big_greedy = BigGreedyCluster()
    big_greedy.get_data(DATA)
    big_greedy.cluster()

