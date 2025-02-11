#В порядке квадратичного отклонения дисперсии максимального
#среднего веса ASCII-кода тройки символов в строке от максимального
#среднего веса ASCII-кода тройки символов в первой строке.
def average_ascii_weight(triplet):
    return sum(ord(char) for char in triplet) / 3

def calculate_statistics_and_deviation(text):

    triplets = [text[i:i+3] for i in range(len(text) - 2)]
    averages = [average_ascii_weight(triplet) for triplet in triplets]

    if not averages:
        return 0, 0

    max_avg = max(averages)
    variance = sum((avg - max_avg) ** 2 for avg in averages) / len(averages)
    deviation = variance ** 0.5
    return max_avg, deviation


first_string = "yfgbib dct c jlyjq aeyrbb"
reference_max, _ = calculate_statistics_and_deviation(first_string)

strings = ["yfgbib dct c jlyjq aeyrbb", "abc def ghi", "xyz uvw rst", "123 456 789"]

sorted_strings = sorted(strings, key=lambda s: (calculate_statistics_and_deviation(s)[0] - reference_max)**2)

for string in sorted_strings:
    max_avg, deviation = calculate_statistics_and_deviation(string)
    deviation_squared = (max_avg - reference_max)**2
    print(f"Строка: '{string}', Макс. средний вес: {max_avg}, Квадр. отклонение: {deviation_squared}")