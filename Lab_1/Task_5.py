#Дана строка. Необходимо найти все даты, которые описаны в
#виде "31 февраля 2007".

def find_dates(text):
    month = {
        "января",
        "февраля",
        "марта",
        "апреля",
        "мая",
        "июня",
        "июля",
        "августа",
        "сентября",
        "октября",
        "ноября",
        "декабря"
    }

    array_text = text.split()
    for i in range(0, len(array_text)):
        a = array_text[i]
        if array_text[i] in month:
            if int(array_text[i-1]) in range(1,32):
                print(f"{array_text[i-1]} {array_text[i]} {array_text[i+1]}")

    return 1

text1 = "Пример 7 февраля 2007 и 18 октября 2008, и также 15 марта 2023 года."


find_dates(text1)

