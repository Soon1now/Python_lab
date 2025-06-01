import sys

def read_input(file):
    with open(file) as f:
        N, K, V = map(int, f.readline().strip().split())
        stations = [list(map(int, f.readline().strip().split())) for _ in range(N)]
    return N, K, V, stations

def calculate(N, K, V, stations):
    stations = [(s, (i + V - 1) // V) for s, i in stations]

    min_price = sys.maxsize
    best_position = 0

    for position in range(K):
        current_price = 0

        for station, trips in stations:
            current_price += min(abs(position - station), K - abs(position - station)) * trips

        if current_price < min_price:
            min_price = current_price
            best_position = position

    return best_position, min_price

N1, K1, V1, stations1 = read_input('D:/Учеба/Python/Lab_4/Task27-123a.txt')
N2, K2, V2, stations2 = read_input('D:/Учеба/Python/Lab_4/Task27-123b.txt')

best_position_1, min_price_1 = calculate(N1, K1, V1, stations1)
print(f"Решение для файла А \nМинимальные затраты : {min_price_1}, Позиция хранилища: {best_position_1}")

best_position_2, min_price_2 = calculate(N2, K2, V2, stations2)
print(f"Решение для файла B \nМинимальные затраты : {min_price_2}, Позиция хранилища: {best_position_2}")
