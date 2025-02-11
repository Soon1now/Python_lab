# Функция 2 Найти максимальную цифры числа, не делящуюся на 3
def min_num(number):

    max_digit = -1
    for i in number:
        digit = int(i)
        if digit % 3 != 0:
            max_digit = max(max_digit,digit)
    return  max_digit if max_digit >= 0 else None

print("введите число")
x = str(input())

result = min_num(x)
if result == None:
    print(f"Все цифры числа кратны 3")
else:
    print(f"Максимальная цифра числа {x}, не кратная 3 равна {result}")