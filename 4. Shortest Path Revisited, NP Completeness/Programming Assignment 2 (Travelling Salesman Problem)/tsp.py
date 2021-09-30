import matplotlib.pyplot as plt
import itertools
import math
import time


DATA = "tsp.txt"


class TravelingSalesman:
    def __init__(self):
        self.number_cities = None
        self.cities = set()
        self.index_to_cities = dict()
        self.index_to_cities_distance = None

    def get_number_cities(self):
        return self.number_cities

    def get_cities(self):
        return self.cities

    def get_index_to_cities(self):
        return self.index_to_cities

    def get_city_x(self, city):
        return city[0]

    def get_city_y(self, city):
        return city[1]

    def get_cities_distance(self, city_1, city_2):
        x1, y1 = self.get_city_x(city_1), self.get_city_y(city_1)
        x2, y2 = self.get_city_x(city_2), self.get_city_y(city_2)

        distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        return distance

    def get_cities_distance_from_index(self, index1, index2):
        return self.index_to_cities_distance[index1][index2]

    def get_data(self, data):
        file = open(data, "r")
        file_list = file.readlines()

        for i in range(0, len(file_list)):
            if i == 0:
                self.number_cities = int(file_list[i])
            else:
                x, y = file_list[i].split()
                x, y = float(x), float(y)
                self.set_city(x, y, i)

        self.calculate_all_distances()

    def set_city(self, x, y, i):
        city = (x, y)
        self.index_to_cities[i] = city

    def calculate_all_distances(self):
        number_cities = self.get_number_cities()
        index_to_cities = self.get_index_to_cities()

        # Create a nested dictionary to store distances between index1 and index2
        distances = {index1: {index2: 0 for index2 in range(1, number_cities+1)} for index1 in range(1, number_cities+1)}

        for i in range(1, number_cities+1):
            for j in range(1, number_cities+1):
                city1, city2 = index_to_cities[i], index_to_cities[j]
                distance = self.get_cities_distance(city1, city2)
                distances[i][j] = distance
                distances[j][i] = distance

        self.index_to_cities_distance = distances

    def plot_cities(self):
        cities = self.get_cities()
        x, y = [], []

        for city in cities:
            coord_x, coord_y = self.get_city_x(city), self.get_city_y(city)
            x.append(coord_x)
            y.append(coord_y)

        #Splitting into 2 smaller subproblems
        number_cities = self.get_number_cities()
        half_number_cities = int(0.5 * number_cities)

        fig = plt.figure()
        ax1 = fig.add_subplot(2, 1, 1)
        ax2 = fig.add_subplot(2, 2, 3)
        ax3 = fig.add_subplot(2, 2, 4, sharey=ax2)
        plt.setp(ax3.get_yticklabels(), visible=False)

        ax1.scatter(x, y)
        ax2.scatter(x[0:half_number_cities], y[0:half_number_cities])
        ax3.scatter(x[half_number_cities:], y[half_number_cities:])
        plt.show()

    def get_subproblems(self, size):
        number_cities = self.get_number_cities()
        subproblems_list = []

        cities = tuple(range(2, number_cities+1))
        subproblems = itertools.combinations(cities, size-1)

        for subproblem in subproblems:
            subproblem = set(subproblem)
            subproblem.add(1)
            subproblem = frozenset(subproblem)
            subproblems_list.append(subproblem)

        return subproblems_list

    def expand_array(self, array, subproblems):
        number_cities = self.get_number_cities()
        new_array = {subproblem: {i: math.inf for i in range(1, number_cities+1)} for subproblem in subproblems}
        array.update(new_array)
        return array

    def set_base_case(self, array, subproblems):
        if len(subproblems[0]) == 2:
            for subproblem in subproblems:
                for i in subproblem:
                    if i != 1:
                        array[subproblem][i] = self.get_cities_distance_from_index(1, i)

        else:
            for subproblem in subproblems:
                if subproblem == frozenset([1]):
                    array[subproblem][1] = 0
                else:
                    array[subproblem][1] = math.inf
        return array

    def get_min_subproblem_distance(self, array, subproblems):
        for subproblem in subproblems:
            for j in subproblem:
                distances = []
                if j != 1:
                    #Iterate through all possible destinations
                    for k in subproblem:
                        if k != 1 and k != j:
                            s = set(subproblem)
                            s.remove(j)
                            s = frozenset(s)
                            value = array[s][k] + self.get_cities_distance_from_index(k, j)
                            distances.append(value)

                    if distances:
                        array[subproblem][j] = min(distances)
        return array

    def solve(self):
        number_cities = self.get_number_cities()

        print("Initialising storage array...")
        array = dict()

        print("Solving in progress...")
        for m in range(2, number_cities+1):
            print(f"Solving subproblems of size m={m}")
            subproblems = self.get_subproblems(size=m)

            # Expanding array to store new subproblem solutions
            array = self.expand_array(array, subproblems)

            # Setting base case for each subproblem
            array = self.set_base_case(array, subproblems)

            # Solving all subproblems
            array = self.get_min_subproblem_distance(array, subproblems)

            # Removing unneeded subproblems
            if m >= 4:
                subproblems_to_remove = self.get_subproblems(size=m-2)
                for subproblem in subproblems_to_remove:
                    array.pop(subproblem)

        # Final step to solve problem
        final_subproblem = frozenset(range(1, number_cities+1))
        final_distances = []
        for j in final_subproblem:
            final_distance = array[final_subproblem][j] + self.get_cities_distance_from_index(j, 1)
            final_distances.append(final_distance)

        print("All computations complete")

        return min(final_distances)


if __name__ == "__main__":
    start_time = time.time()

    tsp = TravelingSalesman()
    tsp.get_data(DATA)
    result = tsp.solve()

    print(f"The shortest Traveling Salesman path has distance {result}")
    print(f"Rounding down to the nearest integer, {int(result)} should be keyed in as the answer")

    end_time = time.time()
    print(f"The script had a runtime of {end_time-start_time} seconds")

    file = open("result.txt", 'w')
    file.write(str(result))
    file.write(f"The script had a runtime of {end_time-start_time} seconds")
    file.close()
