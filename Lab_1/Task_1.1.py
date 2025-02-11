# Функция 1 Найти количество четных чисел, не взаимно простых с данным.

def divisors(number):
    result = {number}

    for i in range(2, number // 2 + 1):
        if number % i == 0:
            result.add(i)
    return result

def cnt_double_divisors(div1, div2):

    common_divisors = div1.intersection(div2)
    return len(common_divisors)


def found_numbers( number, limit ):
    number_divisors = divisors(number)
    cnt_number = 0

    for n in range(2, limit+1):
        if n % 2 == 0:
            n_divisors = divisors(n)
            count_div = cnt_double_divisors(number_divisors,n_divisors)
            if count_div > 0:
                #print(n)
                cnt_number += 1
    return cnt_number

print("Введите число: ")
x = int(input())

print("Введите предел чисел: ")
limit = int(input())

result = found_numbers(x,limit)
print(f"Колличество чисел, не являющихся взаимно простыми с {x} равно {result} ")
