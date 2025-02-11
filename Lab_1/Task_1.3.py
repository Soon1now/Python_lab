# Функция 3 Найти произведение максимального числа, не взаимно
# простого с данным, не делящегося на наименьший делитель исходно числа, и
# суммы цифр числа, меньших 5
import math

def found_sum(number, limit):
    max_number = 0
    result = 0
    sum_digit = sum(int(i) for i in str(number) if int(i)<5)
    min_digit = next(i for i in range(2, number + 1) if number % i == 0)

    for i in range( 1, limit + 1):
        if (math.gcd(number,i) > 1 ):
            if ( i % min_digit != 0 ):
              max_number = i

    if max_number != 0:
        result = max_number * sum_digit
        print(f"Произведение равно {result}")
    else:
        print("Под вашу условие не подошло ни одно число")


print("Введите число: ")
x = int(input())

print("Введите предел чисел: ")
limit = int(input())

found_sum(x, limit)