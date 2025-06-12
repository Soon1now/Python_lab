import sqlite3
import sys

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)
print("Content-Type: text/html; charset=utf-8\n")

print("""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Список танцоров</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f5f5f5;
            margin: 0;
            padding: 20px;
            color: #333;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }
        h1 {
            color: #6a1b9a;
            text-align: center;
            margin-bottom: 30px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 25px 0;
        }
        th, td {
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #9c4dcc;
            color: white;
        }
        tr:hover {
            background-color: #f5f0fa;
        }
        .form-container {
            background-color: #f9f4ff;
            padding: 20px;
            border-radius: 8px;
            margin-top: 30px;
        }
        input[type="text"], input[type="number"], select {
            width: 100%;
            padding: 10px;
            margin: 8px 0;
            display: inline-block;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-sizing: border-box;
        }
        input[type="submit"] {
            background-color: #6a1b9a;
            color: white;
            padding: 12px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }
        input[type="submit"]:hover {
            background-color: #4a148c;
        }
        .action-buttons {
            display: flex;
            gap: 10px;
        }
        .action-btn {
            padding: 5px 10px;
            border-radius: 4px;
            text-decoration: none;
            color: white;
            font-size: 14px;
        }
        .edit-btn {
            background-color: #2196F3;
        }
        .delete-btn {
            background-color: #f44336;
        }
        .back-btn {
            display: inline-block;
            margin-top: 20px;
            background-color: #757575;
            color: white;
            padding: 10px 15px;
            text-decoration: none;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Список танцоров студии</h1>

        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Имя</th>
                    <th>Возраст</th>
                    <th>Действия</th>
                </tr>
            </thead>
            <tbody>
""")

conn = sqlite3.connect('dances.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM Dancers")
dancers = cursor.fetchall()

for dancer in dancers:
    print(f"""
                <tr>
                    <td>{dancer[0]}</td>
                    <td>{dancer[1]}</td>
                    <td>{dancer[2]}</td>
                    <td class="action-buttons">
                        <a href="/cgi-bin/delete_dancers.py?id={dancer[0]}" class="action-btn delete-btn">🗑️</a>
                        <a href="/cgi-bin/edit_dancers.py?id={dancer[0]}" class="action-btn edit-btn">✏️</a>
                    </td>
                </tr>
    """)

print("""
            </tbody>
        </table>

        <div class="form-container">
            <h2>Добавить нового танцора</h2>
            <form action='/cgi-bin/add_dancers.py' method='post'>
                <label for="name">Имя:</label>
                <input type="text" id="name" name="name" required>

                <label for="age">Возраст:</label>
                <input type="number" id="age" name="age" required>

                <label for="group">Группа:</label>
                <select id="group" name="group">
                    <option value="">-- Выберите группу --</option>
    """)


cursor.execute("SELECT dance_id, dance_name FROM Groups")
groups = cursor.fetchall()
for group in groups:
    print(f'<option value="{group[0]}">{group[1]}</option>')

print("""
                </select>

                <input type="submit" value="Добавить танцора">
            </form>
        </div>

        <a href="/cgi-bin/dance.py" class="back-btn">Вернуться на главную</a>
    </div>
</body>
</html>
""")
conn.close()