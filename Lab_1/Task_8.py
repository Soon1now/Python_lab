# 15 Дана строка. Необходимо подсчитать количество цифр в этой строке,
# значение которых больше 5
def cnt_number(text):
    cnt = sum(1 for i in text if int(i)>5)
    return cnt

str = "1338025998428363"
result = cnt_number(str)
print(result)