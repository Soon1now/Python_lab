n = int(input("Введите максимальное число: "))
possible_numbers = set(range(1, n + 1))


def respond_to_question(question, possible_numbers):

    question_numbers = set(map(int, question.split()))

    if len(question_numbers) <= len(possible_numbers) // 2:
        return "NO"

    if possible_numbers.intersection(question_numbers):
        return "YES"
    else:
        return "NO"

while True:
    question = input("Введите вопрос (или HELP для завершения): ")
    if question == "HELP":
        break

    response = respond_to_question(question, possible_numbers)
    print(response)

    question_numbers = set(map(int, question.split()))

    if response == "YES":
        possible_numbers.intersection_update(question_numbers)
    elif response == "NO":
        possible_numbers.difference_update(question_numbers)
    print(f"Возможные числа: {possible_numbers}")

remaining_numbers_sorted = sorted(possible_numbers)
print(" ".join(map(str, remaining_numbers_sorted)))
