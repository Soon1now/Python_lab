import csv
import chrono
from datetime import datetime


def time_to_seconds(time_str):
    if not isinstance(time_str, str):
        return 0
    total_seconds = 0
    parts = time_str.split()
    for i in range(0, len(parts), 2):
        value = int(parts[i]) if parts[i].isdigit() else 0
        unit = parts[i + 1] if i + 1 < len(parts) else ''
        if 'ч.' in unit:
            total_seconds += value * 3600
        elif 'мин.' in unit:
            total_seconds += value * 60
        elif 'сек.' in unit:
            total_seconds += value
    return total_seconds


def parse_date(date_str):
    if not isinstance(date_str, str):
        return None
    try:
        return chrono.parseDate(date_str)
    except:
        return None


def process_csv(file_path, min_time_str, target_score):
    min_time_seconds = time_to_seconds(min_time_str)
    people = []

    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Фамилия'].startswith('Среднее') or row['Фамилия'].startswith('Общее'):
                continue

            try:
                score = float(row['Оценка/10,00'].replace(',', '.'))
            except (ValueError, KeyError):
                continue

            time_spent = time_to_seconds(row['Затраченное время'])

            if score == target_score and time_spent > min_time_seconds:
                people.append({
                    'Фамилия': row['Фамилия'],
                    'Имя': row['Имя'],
                    'Email': row['Адрес электронной почты'],
                    'Time': row['Затраченное время'],
                    'Score': score
                })

    people.sort(key=lambda x: x['Фамилия'])

    return people


def main():
    file_path = '14 - 1.csv'
    min_time = '15 мин.'
    target_score = 9.0

    result = process_csv(file_path, min_time, target_score)

    print(
        f"Количество людей, выполнивших тест более чем за {min_time} и набравших ровно {target_score} баллов: {len(result)}")
    print("\nСписок:")
    for person in result:
        print(
            f"{person['Фамилия']} {person['Имя']}, Email: {person['Email']}, Время: {person['Time']}, Баллы: {person['Score']}")


if __name__ == "__main__":
    main()