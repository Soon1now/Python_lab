#7 В порядке увеличения разницы между количеством сочетаний
#«гласная-согласная» и «согласная-гласная» в строке.


def count_pairs(strings):
    vowels = "аеёиоуыэюяАЕЁИОУЫЭЮЯ"
    consonants = "бвгдежзийклмнопрстфхцчшщБВГДЕЖЗИЙКЛМНОПРСТФХЦЧШЩ"



    results = []
    for string in strings:
        vc_count = 0
        cv_count = 0

        for i in range(len(string) - 1):
            if (string[i] in vowels) and (string[i+1] in consonants):
                vc_count += 1
            elif (string[i+1] in vowels) and (string[i] in consonants):
                cv_count += 1
        difference = vc_count - cv_count
        results.append((string,difference))

    results.sort(key=lambda x: x[1])

    return results


strings = [
    "Пример строки",
    "София",
    "Политех лучше всех"
]

result = count_pairs(strings)

for s, diff in result:
    print(f"Строка: '{s}', Разница: {diff}")
