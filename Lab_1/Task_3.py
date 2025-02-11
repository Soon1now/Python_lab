#Дана строка в которой записаны слова через пробел. Необходимо
#посчитать количество слов.

def count_words(string):
    words = string.split()
    return len(words)

print("Введите строку в которой слова записаны через пробел")
str = str(input())
result = count_words(str)
print(f"Количество слов: {result}")
