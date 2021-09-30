DATA = 'huffman.txt'


class Huffman:
    def __init__(self):
        self.number_symbols = 0
        self.weights = []
        self.nodes = []
        self.codes = {}

    def get_number_symbols(self):
        return self.number_symbols

    def get_weights(self):
        return self.weights

    def get_nodes(self):
        return self.nodes

    def get_data(self, filename):
        file = open(filename, "r")
        file_list = file.readlines()

        weights = []

        for i in range(0, len(file_list)):
            if i == 0:
                number_symbols = file_list[i]
                self.set_number_symbols(int(number_symbols))

            else:
                weights.append((i, int(file_list[i])))
                node_index = i
                node_weight = int(file_list[i])
                node = Node(data=node_index, weight=node_weight)

        self.set_weights(weights)

    def set_number_symbols(self, number):
        self.number_symbols = number

    def set_weights(self, weights):
        self.weights = weights

    def set_nodes(self, nodes):
        self.nodes = nodes

    def set_code(self, node_data, code):
        self.codes[node_data] = code

    def set_weights_ascending_order(self):
        weights = self.get_weights()
        weights.sort(key=lambda x: x[1])
        self.set_weights(weights)

    def initialise_nodes(self):
        self.set_weights_ascending_order()
        weights = self.get_weights()
        nodes = []
        for node_index, node_weight in weights:
            node = Node(data=node_index, weight=node_weight)
            nodes.append(node)
        self.set_nodes(nodes)

    def build_tree(self):
        self.initialise_nodes()
        queue1 = self.get_nodes().copy()
        queue2 = []

        while len(queue1) + len(queue2) != 1:
            # Dequeue two nodes with the minimum frequency by examining the front of both queues, using the algo below:
            compared_nodes = []
            while len(compared_nodes) != 2:
                # If second queue is empty, dequeue from first queue
                if len(queue2) == 0:
                    compared_nodes.append(queue1.pop(0))

                # If first queue is empty, dequeue from second queue
                elif len(queue1) == 0:
                    compared_nodes.append(queue2.pop(0))

                # Else, compare the front of two queues and dequeue the minimum.
                else:
                    node1_weight = queue1[0].get_weight()
                    node2_weight = queue2[0].get_weight()
                    if node1_weight < node2_weight:
                        compared_nodes.append(queue1.pop(0))
                    elif node2_weight < node1_weight:
                        compared_nodes.append(queue2.pop(0))

            # Create a new internal node with frequency equal to the sum of the two nodes frequencies.
            node1 = compared_nodes.pop(0)
            node2 = compared_nodes.pop(0)
            internal_node_weight = node1.get_weight() + node2.get_weight()
            internal_node = Node(data='$', weight=internal_node_weight)

            # Make the first Dequeued node as its left child and the second Dequeued node as right child.
            internal_node.set_child_left(node1)
            internal_node.set_child_right(node2)

            # Enqueue new internal node to second queue
            queue2.append(internal_node)

        root_node = queue2.pop(0)
        root_node = self.encode_nodes(root_node=root_node, code='')
        return root_node

    def encode_nodes(self, root_node, code):
        if root_node.get_child_left() is not None:
            self.encode_nodes(root_node=root_node.get_child_left(), code=code + '0')

        if root_node.get_child_right() is not None:
            self.encode_nodes(root_node=root_node.get_child_right(), code=code + '1')

        if root_node.isLeaf():
            root_node.set_code(code)
            node_data = root_node.get_data()
            self.set_code(node_data, code)
        return root_node

    def get_maximum_codelength(self, root_node):
        max_node = 0
        max_code_length = 0
        for node in huffman.codes:
            if len(huffman.codes[node]) > max_code_length:
                max_code_length = len(huffman.codes[node])
                max_node = node
        print(f"Maximum code length is {max_code_length}")

    def get_minimum_codelength(self, root_node):
        while root_node.get_child_left():
            root_node = root_node.get_child_left()
        length = len(root_node.get_code())
        print(f"Minimum code length is {length}")


class Node:
    def __init__(self, data, weight):
        self.left = None
        self.right = None
        self.data = data
        self.weight = weight
        self.code = ''

    def get_child_left(self):
        return self.left

    def get_child_right(self):
        return self.right

    def get_data(self):
        return self.data

    def get_weight(self):
        return self.weight

    def get_code(self):
        return self.code

    def set_child_left(self, node):
        self.left = node

    def set_child_right(self, node):
        self.right = node

    def set_code(self, code):
        self.code = code

    def isLeaf(self):
        if self.get_child_left() is None:
            if self.get_child_right() is None:
                return True
        return False

    def print_node(self):
        print(f'Node {self.get_data()} has weight of {self.get_weight()}, and Huffman encoding of {self.get_code()}')
        print(f'Node {self.get_data()} has left child {self.get_child_left().get_data()}, and right child {self.get_child_right().get_data()}')


if __name__ == "__main__":
    huffman = Huffman()
    huffman.get_data(DATA)
    root_node = huffman.build_tree()
    huffman.get_maximum_codelength(root_node)
    huffman.get_minimum_codelength(root_node)
    #print(huffman.codes)

