# Дана строка. Необходимо найти все незадействованные символы
# латиницы в этой строке.
import string

def find_unused_letters(s):
    all_letters = set(string.ascii_lowercase)
    used_letters = set(s.lower())

    unused_letters = all_letters - used_letters
    return sorted(unused_letters)


input_string = "Hello, My name is Sofiya"
result = find_unused_letters(input_string)
print(result)