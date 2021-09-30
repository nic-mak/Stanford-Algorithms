from time import time

FILENAME = 'TwoSum.txt'


class TwoSum:
    def __init__(self):
        self.data = []
        #self.pairs = []
        self.t_values = []
        self.result = 0

    def get_dataset(self, filename):
        #Importing data
        file = open(filename, "r")
        for row in file.readlines():
            value = int(row)
            self.data.append(value)

        #Removing duplicate data
        #self.data = list(dict.fromkeys(self.data))

        #Sorting data
        self.data.sort()

    def get_results(self):
        print(f'Result: {self.result}')

    def get_run_time(self, start, end):
        time_taken = end-start
        print(f'Time taken for the script to run: {time_taken:.2f} seconds')

    def calculate_t(self):
        i, j = 0, len(self.data)-1

        while i < j:
            x, y = self.data[i], self.data[j]
            t = x+y

            if t < -10000:
                i += 1
            elif t > 10000:
                j -= 1
            else:
                j_split = j

                while i < j_split and t >= -10000:
                    if t not in self.t_values:
                        self.t_values.append(t)
                        #self.pairs.append((x,y))
                    j_split -= 1
                    y = self.data[j_split]
                    t = x+y

                i += 1
        self.result = len(self.t_values)

        return len(self.t_values)


if __name__ == '__main__':
    start = time()

    twosum = TwoSum()
    twosum.get_dataset(FILENAME)
    twosum.calculate_t()
    twosum.get_results()

    end = time()

    twosum.get_run_time(start, end)
