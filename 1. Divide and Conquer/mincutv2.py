import random

FILENAME = "kargerMinCut.txt"
NUMBER_OF_TRIALS = 100


def get_array_vertices_from_source(filename):
    #Returns dictionary. dict[i] will give a list of nodes that vertex i is connected to.

    file = open(filename, "r")
    array_vertices = {}

    for row in file.readlines():
        split_row_str = row.split()
        split_row_int = list(map(lambda x: int(x), split_row_str))

        vertex_index = split_row_int[0]
        array_vertices[vertex_index] = split_row_int[1:]

    return array_vertices


def get_random_edge(array_vertices):
    random_index = random.choice(list(array_vertices.keys()))
    random_endpoint = random.choice(array_vertices[random_index])
    return random_index, random_endpoint


def merge_vertices(vertex1, vertex2, array_vertices):
    # Supernode created will assume index of vertex1
    connections_vertex1 = array_vertices[vertex1]
    connections_vertex2 = array_vertices[vertex2]
    connections_vertex1.extend(connections_vertex2)
    del array_vertices[vertex2]

    #Find all vertex2 and replace with vertex1
    for vertex in array_vertices:
        new_connections = []

        for connection in array_vertices[vertex]:
            if connection == vertex2:
                new_connections.append(vertex1)
            else:
                new_connections.append(connection)

        array_vertices[vertex] = new_connections

    #Remove self loops
    new_connections = []
    for connection in array_vertices[vertex1]:
        if connection != vertex1:
            new_connections.append(connection)
    array_vertices[vertex1] = new_connections

    return array_vertices


def randomised_contraction(array_vertices):
    while len(array_vertices) > 2:
        random_vertex1, random_vertex2 = get_random_edge(array_vertices)
        new_array_vertices = merge_vertices(vertex1=random_vertex1, vertex2=random_vertex2, array_vertices=array_vertices)
        #Don't need to remove self loops as they are accounted for in merge

    return new_array_vertices


def min_cut(filename, number_of_trials):
    number_of_cuts = []

    for i in range(number_of_trials):
        array_vertices = get_array_vertices_from_source(filename)
        final_array_vertices = randomised_contraction(array_vertices)

        for vertex in final_array_vertices:
            number_of_edges = len(final_array_vertices[vertex])
            number_of_cuts.append(number_of_edges)

    return min(number_of_cuts)


print(min_cut(FILENAME, NUMBER_OF_TRIALS))


