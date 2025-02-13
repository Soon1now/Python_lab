#Дан целочисленный массив. Необходимо найти минимальный четный элемент.
def found_numbers(arr):

    result = min(i for i in arr if i % 2 == 0)
    return  result

array  = [8,9,6,3,6,9,3,1,4,6,9]
print(found_numbers(array))