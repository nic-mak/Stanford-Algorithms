import math

DATA = 'jobs.txt'


class MinWeightCompletion:
    def __init__(self, filename):
        self.filename = filename
        self.number_of_jobs = 0
        self.jobs = {}
        self.wl_index = []

    def get_filename(self):
        return self.filename

    def get_data(self):
        file = open(self.get_filename(), "r")

        file_list = file.readlines()
        jobs = {}
        wl_index = [-math.inf]
        for i in range(0, len(file_list)):
            if i == 0:
                self.set_number_of_jobs(int(file_list[i]))
            else:
                weight, length = file_list[i].split()
                weight, length = int(weight), int(length)
                wl_index.append(self.calculate_wl_index(weight, length))
                jobs[i] = (weight, length)

        self.set_wl_index(wl_index)
        self.set_jobs(jobs)

    def get_wl_index(self):
        return self.wl_index

    def get_jobs(self):
        return self.jobs

    def set_number_of_jobs(self, number):
        self.number_of_jobs = number

    def set_wl_index(self, index):
        self.wl_index = index

    def set_jobs(self, jobs):
        self.jobs = jobs

    def calculate_wl_index(self, weight, length):
        return weight/length

    def calculate_weighted_completion_time(self):
        jobs = self.get_jobs()
        jobs_added = 0
        wl_index = self.get_wl_index().copy()

        total_completion_time = 0
        total_weighted_completion_time = 0
        while jobs_added < self.number_of_jobs:
            job, index = self.get_max_index_job(wl_index)
            wl_index[job] = -math.inf

            job_weight = jobs[job][0]
            total_completion_time += jobs[job][1]
            total_weighted_completion_time += (job_weight * total_completion_time)

            jobs_added += 1

        return total_weighted_completion_time


    def get_max_index_job(self, wl_index):
        job = None
        index = -math.inf

        for i in range(1, len(wl_index)):
            if wl_index[i] == -math.inf:
                pass

            elif wl_index[i] > index:
                job = i
                index = wl_index[i]

            elif wl_index[i] == index:
                jobs = self.get_jobs()

                weight_original = jobs[job]
                weight_new = jobs[i]

                if weight_new > weight_original:
                    job = i

        return job, index


analyser = MinWeightCompletion(DATA)
analyser.get_data()
weighted_completion_time = analyser.calculate_weighted_completion_time()
print(weighted_completion_time)
