#4 Дан целочисленный массив. Вывести индексы массива в том порядке, в котором соответствующие
# им элементы образуют убывающую последовательность.

def sorted_indices(arr):
    index_arr = list(range(0, len(arr)))
    index_arr.sort(key = lambda x : arr[x], reverse=True)
    return index_arr

array = [2,1,5,3]
result = sorted_indices(array)

print("Индексы в порядке убывания значений:", result)
