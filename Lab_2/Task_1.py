def respond_to_question(question, possible_numbers):

    question_numbers = set(map(int, question.split()))

    if len(question_numbers) <= len(possible_numbers) // 2:
        return "NO"

    if possible_numbers.intersection(question_numbers):
        return "YES"
    else:
        return "NO"
