import math
import time


DATA = "data.txt"


class GreedyTravelingSalesman:
    def __init__(self):
        self.number_cities = 0
        self.index_to_city = dict()

    def get_number_cities(self):
        return self.number_cities

    def get_city_x(self, city):
        return city[0]

    def get_city_y(self, city):
        return city[1]

    def get_city_from_index(self, index):
        return self.index_to_city[index]

    def get_distance_from_index(self, index1, index2):
        city1, city2 = self.get_city_from_index(index1), self.get_city_from_index(index2)
        x1, y1 = self.get_city_x(city1), self.get_city_y(city1)
        x2, y2 = self.get_city_x(city2), self.get_city_y(city2)

        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def get_data(self, data):
        file = open(data, "r")
        file_list = file.readlines()

        for i in range(0, len(file_list)):
            if i == 0:
                self.number_cities = int(file_list[i])
            else:
                index, x, y = file_list[i].split()
                index, x, y = int(index), float(x), float(y)
                self.set_city(x, y, index)

    def set_city(self, x, y, index):
        self.index_to_city[index] = (x, y)

    def solve(self):
        print("Starting solver!")
        number_cities = self.get_number_cities()
        cities_to_visit = list(range(2, number_cities + 1))

        current_city, current_min_city = 1, 1
        current_min_distance = math.inf
        total_distance = 0

        while len(cities_to_visit) != 0:

            if len(cities_to_visit) in [10000, 20000, 30000]:
                print(f"{len(cities_to_visit)} cities left to visit")

            for city in cities_to_visit:
                distance = self.get_distance_from_index(current_city, city)
                if distance == current_min_distance:
                    current_min_city = min(current_min_city, city)
                elif distance < current_min_distance:
                    current_min_distance = distance
                    current_min_city = city

            current_city = current_min_city
            cities_to_visit.remove(current_min_city)
            total_distance += current_min_distance
            current_min_distance = math.inf

        total_distance += self.get_distance_from_index(current_city, 1)
        return total_distance


if __name__ == "__main__":
    start_time = time.time()

    tsp = GreedyTravelingSalesman()
    tsp.get_data(DATA)
    result = tsp.solve()

    print(f"The shortest Traveling Salesman path has distance {result}")
    print(f"Rounding down to the nearest integer, {int(result)} should be keyed in as the answer")

    end_time = time.time()
    print(f"The script had a runtime of {end_time-start_time} seconds")
    '''
    file = open("result.txt", 'w')
    file.write(str(result))
    file.write(f"The script had a runtime of {end_time-start_time} seconds")
    file.close()
    '''
