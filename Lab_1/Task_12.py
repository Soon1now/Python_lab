#В порядке увеличения квадратичного отклонения
#частоты встречаемости самого часто встречаемого в строке символа от частоты его
#встречаемости в текстах на этом алфавите.
def calculate_frequencies(text, input_string):

    string_freq = {}
    for char in input_string:
        string_freq[char] = string_freq.get(char, 0) + 1

    text_freq = {}
    for char in text:
        text_freq[char] = text_freq.get(char, 0) + 1

    deviations = []

    for char in string_freq.keys():
        f_string = string_freq[char]
        f_text = text_freq.get(char, 0)

        d_squared = (f_string - f_text) ** 2
        deviations.append((char, d_squared))


    deviations.sort(key=lambda item: item[1])

    return deviations


# Пример использования
text = "другой пример текста, который мы анализируем"
input_string = "текста"
result = calculate_frequencies(text, input_string)

for char, dev in result:
    print(f"Символ: '{char}', Квадратное отклонение: {dev}")
