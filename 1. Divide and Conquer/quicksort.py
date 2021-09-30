FILENAME = "quicksort.txt"

ODD = "odd"
EVEN = "even"

ELEMENT_FIRST = "first_element"
ELEMENT_LAST = "last_element"
ELEMENT_MEDIAN = "median_element"

PIVOT_ELEMENT_MODE = ELEMENT_MEDIAN

COUNT_COMPARISONS = 0


def quicksort(array, n):
    global COUNT_COMPARISONS

    if n == 1:
        return array

    else:
        boundary_index = partition(array, 0, n-1)
        COUNT_COMPARISONS += (n-1)

        array1, array2 = array[0:boundary_index], array[boundary_index+1:]  #excludes pivot
        array1_length, array2_length = get_array_length(array1), get_array_length(array2)

        if array1_length != 0:
            array1 = quicksort(array1, array1_length)

        if array2_length != 0:
            array2 = quicksort(array2, array2_length)

    return array1 + [array[boundary_index]] + array2


def partition(array, bound_index_left, bound_index_right):
    array, pivot_element = get_modified_array_and_pivot_element(array, bound_index_left, bound_index_right, mode=PIVOT_ELEMENT_MODE)

    i = bound_index_left+1

    for j in range(bound_index_left+1, bound_index_right+1):
        if array[j] < pivot_element:
            swap(array, index1=i, index2=j)
            i += 1

    #swap pivot to the correct position
    swap(array, index1=bound_index_left, index2=i-1)

    return i-1  #returns index of where pivot is now


def swap(array, index1, index2, inplace=True):
    array[index1], array[index2] = array[index2], array[index1]

    if inplace is False:
        return array


def get_modified_array_and_pivot_element(array, bound_index_left, bound_index_right, mode):
    if mode == ELEMENT_FIRST:
        pivot_element = get_array_first_element(array, bound_index_left)[0]

    elif mode == ELEMENT_LAST:
        pivot_element = get_array_last_element(array, bound_index_right)[0]
        swap(array, bound_index_left, bound_index_right)

    elif mode == ELEMENT_MEDIAN:
        three_values = [get_array_first_element(array, bound_index_left), get_array_middle_element(array), get_array_last_element(array, bound_index_right)]
        ## Three values is a list containing 3 tuples of (value from array, index where value is found)
        pivot_element, pivot_element_index = get_array_median_element_and_index(three_values)
        swap(array, bound_index_left, pivot_element_index)

    return array, pivot_element


def get_array_length(array):
    return len(array)


def get_array_length_odd_or_even(array):
    if get_array_length(array)%2 == 0:
        return EVEN
    else:
        return ODD


def get_array_middle_element(array):
    array_length = get_array_length(array)

    if get_array_length_odd_or_even(array) == ODD:
        middle_element_index = array_length//2

    elif get_array_length_odd_or_even(array) == EVEN:
        middle_element_index = int(array_length/2-1)

    return array[middle_element_index], middle_element_index


def get_array_first_element(array, bound_index_left):
    return array[bound_index_left], bound_index_left


def get_array_last_element(array, bound_index_right):
    return array[bound_index_right], bound_index_right


def get_array_median_element_and_index(array):
    #Assuming input of list with 3 tuples, each containing (value from array, index where value is found)
    values, indexes = [], []

    for value, index in array:
        values.append(value)
        indexes.append(index)

    max_value = max(values)
    min_value = min(values)

    for i in range(len(values)):
        if values[i] != max_value and values[i] != min_value:
            return values[i], indexes[i]

        elif values[i] == values[i+1] and values[i] == min_value:
            return values[i], indexes[i]

        elif values[i] == values[i+1] and values[i] == max_value:
            return values[i], indexes[i]


def import_array(filename):
    file = open(filename, "r")
    input_array = []

    for entry in file.readlines():
        input_array.append(int(entry))

    return input_array


input_array = import_array(FILENAME)
sorted_array = quicksort(input_array, get_array_length(input_array))
#print(sorted_array)
print(COUNT_COMPARISONS)
