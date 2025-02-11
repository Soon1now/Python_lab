#Дано натуральное число. Необходимо найти количество различных
# цифр в его десятичной записи.
def count_unique_digits(n):
    digits = set(str(n))
    return len(digits)

print("Введите чиисло, для подсчета различных цифр: ")
number = int(input())
unique_digit_count = count_unique_digits(number)
print(f"Количество различных цифр: {unique_digit_count}")