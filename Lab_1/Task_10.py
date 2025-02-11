#Задание 10 Дан список строк с клавиатуры. Упорядочить по количеству
#слов в строке.
def sort_strings():
    strings = []
    print("Введите строки (для завершения ввода введите пустую строку):")

    while True:
        line = input()
        if line=="":
            break
        strings.append(line)

    sorted_strings = sorted(strings, key= lambda string: len(string.split()))

    print("Строки, упорядоченные по количеству слов:")
    for s in sorted_strings:
        print(s)

sort_strings()