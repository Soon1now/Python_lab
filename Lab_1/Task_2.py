#Дана строка. Необходимо проверить, является ли она палиндромом.
def string_palindrome( str ):

    if len(str) % 2 == 0:
        lenght = len(str) // 2 -1
    else:
        lenght = len(str) // 2

    for i in range(0, lenght):
        if str[i] != str[len(str) - 1 - i]: return 0
    return 1

print("Введите число на проверку палиндрома: ")
string = str(input())
result = string_palindrome(string)
if result == 1: print(f"Число {string} является палиндромом")
else: print(f"Число {string} не является палиндромом")