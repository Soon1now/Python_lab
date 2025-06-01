def count_word(file, word1, word2):
    with open(file, encoding='utf-8') as f:
        text = f.read()

    text_lower = text.lower().replace(".", "").replace(",", "")
    word1_lower = word1.lower()
    word2_lower = word2.lower()

    cnt_word1 = text_lower.count(word1_lower)
    cnt_word2 = text_lower.count(word2_lower)

    cnt_double = text_lower.count(f"{word1_lower} {word2_lower}") + text_lower.count(f"{word2_lower} {word1_lower}")

    return cnt_word1, cnt_word2, cnt_double

result = count_word('D:/Учеба/Python/Lab_4/Task_2.txt', "день", "ясный")
print(f"'день' встречается: {result[0]} раз(а)")
print(f"'ясный' встречается: {result[1]} раз(а)")
print(f"Соседние вхождения: {result[2]} раз(а)")

