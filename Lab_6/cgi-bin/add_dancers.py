import sqlite3, cgi, sys

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)
print("Content-Type: text/html; charset=utf-8\n")

form = cgi.FieldStorage()
name = form.getvalue("name")
age = form.getvalue("age")

conn = sqlite3.connect('dances.db')
cursor = conn.cursor()
cursor.execute("INSERT INTO Dancers (name, age) VALUES (?, ?)", (name, age))
conn.commit()
conn.close()

print("""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="2;url=/cgi-bin/dancers.py">
    <title>Добавление танцора</title>
</head>
<body>
    <h1>Танцор добавлен!</h1>
    <p>Вы будете перенаправлены обратно через 2 секунды...</p>
</body>
</html>
""")

