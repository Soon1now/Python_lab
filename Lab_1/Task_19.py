#Для введенного числа построить список всех его простых делителей,
# причем если введенное число делится на простое число p в степени α,
# то в итоговом списке число p должно повторяться α раз.
# Результирующий список должен быть упорядочен по возрастанию.
def prime_factorization(n):

    if n <= 1:
        return []

    factors = []
    d = 2

    while d * d <= n:
        while n % d == 0:
            factors.append(d)  #
            n //= d
        d += 1

    if n > 1:
        factors.append(n)

    return factors


number = 52
prime_factors = prime_factorization(number)
print(f"Простые делители числа {number}: {prime_factors}")

number = 1
prime_factors = prime_factorization(number)
print(f"Простые делители числа {number}: {prime_factors}")