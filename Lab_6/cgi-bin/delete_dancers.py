import sqlite3, cgi, sys

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)
print("Content-Type: text/html; charset=utf-8\n")

form = cgi.FieldStorage()
dancer_id = form.getvalue("id")

conn = sqlite3.connect('dances.db')
cursor = conn.cursor()
cursor.execute("DELETE FROM Participation WHERE dancer_id = ?", (dancer_id,))

cursor.execute("DELETE FROM Dancers WHERE dancer_id = ?", (dancer_id,))
conn.commit()
conn.close()

print("""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="2;url=/cgi-bin/dancers.py">
    <title>Удаление танцора</title>
</head>
<body>
    <h1>Танцор удален!</h1>
    <p>Вы будете перенаправлены обратно через 2 секунды...</p>
</body>
</html>
""")