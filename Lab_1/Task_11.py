#1 В порядке увеличения разницы между количеством согласных и
# количеством гласных букв в строке.
def dif_cnt_letter(s):
    vowels = "aeiouyаеёиоуыэюя"
    consonants = "bcdfghjklmnpqrstvwxyzбвгдежзийклмнопрстфхцчшщ"

    cnt_v = sum(1 for i in s if i in vowels)
    cnt_c = sum(1 for i in s if i in consonants)
    return abs(cnt_v-cnt_c)

def sort_strings():
    strings = []
    print("Введите строки (для завершения ввода введите пустую строку):")

    while True:
        line = input()
        if line=="":
            break
        strings.append(line)

    sorted_strings = sorted(strings, key= dif_cnt_letter)

    print("Строки, упорядоченные по разнице между количеством гласных и согласных букв:")
    for s in sorted_strings:
        print(s)

sort_strings()