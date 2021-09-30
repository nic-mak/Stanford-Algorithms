FILENAME = "Median.txt"


class HeapMedian:
    def __init__(self):
        self.stream_overall = []
        self.stream_current = []

    def init_stream(self, filename):
        file = open(filename, "r")
        for row in file.readlines():
            value = int(row)
            self.stream_overall.append(value)

    def get_length_stream_current(self):
        return len(self.stream_current)

    def get_stream_next(self):
        return self.stream_overall.pop(0)

    def get_current_median(self):
        length_stream_current = self.get_length_stream_current()

        if (length_stream_current % 2) == 0:  #even
            k = int(length_stream_current/2 -1)  #account for 0 based indexing

        else:  #odd
            k = length_stream_current - 1
            k = k/2
            k = int(k)

        return self.stream_current[k]

    def set_stream_current_next(self):
        value = self.get_stream_next()
        self.stream_current.append(value)
        self.stream_current.sort()

    def get_median_sums(self, n):
        medians_list = []
        for i in range(n):
            self.set_stream_current_next()
            median = self.get_current_median()
            medians_list.append(median)

        total_median = sum(medians_list)
        return total_median


heap_median = HeapMedian()
heap_median.init_stream(FILENAME)
print(heap_median.get_median_sums(10000))
