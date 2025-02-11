#Задание 9 Прочитать список строк с клавиатуры. Упорядочить по длине
#строки.

def sort_strings_by_length():
    strings = []
    print("Введите строки (для завершения ввода введите пустую строку):")

    while True:
        line = input()
        if line=="":
            break
        strings.append(line)

    sorted_strings = sorted(strings, key=len)

    print("Строки, упорядоченные по длине:")
    for s in sorted_strings:
        print(s)

sort_strings_by_length()
