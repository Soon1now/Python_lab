#Дан целочисленный массив. Необходимо найти элементы, расположенные между первым и последним максимальным.
from operator import indexOf


def found_numbers(arr):

    max_num = max(i for i in arr)

    index1_max = int(indexOf(arr, max_num))+1
    index2_max = len(arr) - (indexOf(arr[::-1], max_num)) - 1

    return  arr[index1_max: index2_max]
array  = [8,9,6,3,6,9,3,1,4,6,9]
result = found_numbers(array)
print(result)