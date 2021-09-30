import multiprocessing

DATA = 'knapsack1.txt'
DATA_LARGE = 'knapsack_large.txt'


class Knapsack:
    def __init__(self):
        self.knapsack_size = 0
        self.number_items = 0
        self.values = {}
        self.weights = {}

    def get_knapsack_size(self):
        return self.knapsack_size

    def get_number_items(self):
        return self.number_items

    def get_values(self):
        return self.values

    def get_weights(self):
        return self.weights

    def set_values(self, values):
        self.values = values

    def set_weights(self, weights):
        self.weights = weights

    def set_value(self, index, value):
        values = self.get_values()
        values[index] = value
        self.set_values(values)

    def set_weight(self, index, weight):
        weights = self.get_weights()
        weights[index] = weight
        self.set_weights(weights)

    def get_value_from_index(self, index):
        values = self.get_values()
        return values[index]

    def get_weight_from_index(self, index):
        weights = self.get_weights()
        return weights[index]

    def get_data(self, filename):
        file = open(filename, "r")
        file_list = file.readlines()

        for i in range(0, len(file_list)):

            if i == 0:
                knapsack_size, number_items = file_list[i].split()
                self.knapsack_size, self.number_items = int(knapsack_size), int(number_items)

            else:
                value, weight = file_list[i].split()
                self.set_value(index=i, value=int(value))
                self.set_weight(index=i, weight=int(weight))

    def initialise_2d_array(self):
        x = self.get_knapsack_size()

        array = {}
        # Initialise array A, where
        for i in range(0, x+1):
            array[i] = {}

        # A(0,x) = 0, and x = 0,1....x
        for i in range(0, x + 1):
            array[0][i] = 0
        return array

    def allocate(self):
        array = self.initialise_2d_array()
        n = self.get_number_items()
        w = self.get_knapsack_size()

        for i in range(1, n+1):
            for x in range(0, w+1):
                weight = self.get_weight_from_index(index=i)
                value = self.get_value_from_index(index=i)

                # If weight of item is greater than current knapsack size, it cannot be included.
                # Value of array remains the same as the previous item added
                if weight > x:
                    array[i][x] = array[i-1][x]

                else:
                    # Case 1: Item i is not in knapsack. Value of array is the same as previously
                    case1 = array[i-1][x]

                    # Case 2: Item i is in knapsack. Value of array is previous value, plus current item value.
                    case2 = array[i-1][x-weight] + value

                    array[i][x] = max(case1, case2)

        return array[n][w]

    def allocate_large(self):
        # This method is used when the data set is too large for the regular .allocate() method
        n = self.get_number_items()
        w = self.get_knapsack_size()
        array = [0 for i in range(0, w+1)]

        for i in range(1, n+1):
            weight = self.get_weight_from_index(index=i)
            value = self.get_value_from_index(index=i)
            print(f"Solving i={i}")
            for x in range(w, weight, -1):  # Starting from the back
                # Case 1: Item i is not in knapsack. Value of array is the same as previously
                case1 = array[x]

                # Case 2: Item i is in knapsack. Value of array is previous value, plus current item value.
                case2 = array[x-weight] + value
                array[x] = max(case1, case2)

        print(array[w])
        return array[w]


if __name__ == '__main__':
    #knapsack = Knapsack()
    #knapsack.get_data(DATA)
    #print(knapsack.allocate())

    knapsack = Knapsack()
    knapsack.get_data(DATA_LARGE)
    knapsack.allocate_large()
    #4243395

