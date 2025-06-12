#!/usr/bin/env python3
import sqlite3
import cgi
import sys

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)
print("Content-Type: text/html; charset=utf-8\n")

form = cgi.FieldStorage()
dancer_id = form.getvalue('id')

conn = sqlite3.connect('dances.db')
cursor = conn.cursor()

if dancer_id:
    cursor.execute("SELECT * FROM Dancers WHERE dancer_id = ?", (dancer_id,))
    dancer = cursor.fetchone()
else:
    dancer = None

if dancer:
    print(f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Редактировать Танцора</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                padding: 20px;
                background-color: #f0f0f0;
            }}
            .container {{
                background: white;
                padding: 20px;
                border-radius: 10px;
                max-width: 600px;
                margin: auto;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }}
            input[type="text"], input[type="number"] {{
                width: 100%;
                padding: 10px;
                margin-top: 10px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }}            
            input[type="submit"] {{
            background-color: #6a1b9a;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            margin-top: 10px;
        }}
        input[type="submit"]:hover {{
            background-color: #4a148c;
        }}
            a {{
                display: inline-block;
                margin-top: 20px;
                text-decoration: none;
                color: #333;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Редактировать Танцора</h1>
            <form action="/cgi-bin/edit_dancers.py" method="post">
                <input type="hidden" name="dancer_id" value="{dancer[0]}">

                <label for="name">Имя:</label>
                <input type="text" id="name" name="name" value="{dancer[1]}" required>

                <label for="age">Возраст:</label>
                <input type="number" id="age" name="age" value="{dancer[2]}" required>

                <input type="submit" value="Сохранить">
            </form>
        </div>
    </body>
    </html>
    """)
elif form.getvalue('dancer_id') and form.getvalue('name') and form.getvalue('age'):
    # Если пришли данные для сохранения изменений
    dancer_id = form.getvalue('dancer_id')
    name = form.getvalue('name')
    age = form.getvalue('age')

    cursor.execute("""
        UPDATE Dancers
        SET name = ?, age = ?
        WHERE dancer_id = ?
    """, (name, age, dancer_id))

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
        <h1>Танцор обнавлен!</h1>
        <p>Вы будете перенаправлены обратно через 2 секунды...</p>
    </body>
    </html>
    """)

conn.close()
