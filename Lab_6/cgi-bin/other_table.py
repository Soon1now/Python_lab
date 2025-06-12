
import sqlite3, cgi, sys

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)
print("Content-Type: text/html; charset=utf-8\n")

print("""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Сводная таблица | Студия танца I'm Dance Home</title>
    <style>
        :root {
            --primary-color: #6a1b9a;
            --secondary-color: #9c4dcc;
            --light-color: #f5f0fa;
            --text-color: #333;
            --white: #ffffff;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            margin: 0;
            padding: 20px;
            color: var(--text-color);
            line-height: 1.6;
        }

        .container {
            max-width: 1200px;
            margin: 30px auto;
            background: var(--white);
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            padding: 40px;
            overflow-x: auto;
        }

        h1 {
            color: var(--primary-color);
            text-align: center;
            margin-bottom: 10px;
            font-size: 2.5em;
        }

        h2 {
            color: var(--secondary-color);
            text-align: center;
            margin-top: 0;
            margin-bottom: 30px;
            font-weight: 400;
            border-bottom: 2px solid var(--light-color);
            padding-bottom: 15px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin: 25px 0;
            font-size: 1.1em;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.05);
        }

        thead tr {
            background-color: var(--primary-color);
            color: var(--white);
            text-align: left;
            font-weight: bold;
        }

        th, td {
            padding: 15px 20px;
            border-bottom: 1px solid #dddddd;
        }

        tbody tr:nth-of-type(even) {
            background-color: var(--light-color);
        }

        tbody tr:last-of-type {
            border-bottom: 2px solid var(--primary-color);
        }

        tbody tr:hover {
            background-color: #ede7f6;
            transform: scale(1.01);
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            transition: all 0.2s ease;
        }

        .back-btn {
            display: inline-block;
            margin-top: 30px;
            background: var(--primary-color);
            color: var(--white);
            padding: 12px 25px;
            text-decoration: none;
            border-radius: 50px;
            font-weight: 500;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(106, 27, 154, 0.3);
        }

        .back-btn:hover {
            background: var(--secondary-color);
            transform: translateY(-2px);
            box-shadow: 0 7px 20px rgba(106, 27, 154, 0.4);
        }

        .stats {
            display: flex;
            justify-content: space-around;
            margin: 30px 0;
            flex-wrap: wrap;
        }

        .stat-card {
            background: linear-gradient(135deg, var(--secondary-color), var(--primary-color));
            color: var(--white);
            padding: 20px;
            border-radius: 10px;
            width: 200px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            margin: 10px;
        }

        .stat-value {
            font-size: 2em;
            font-weight: bold;
            margin: 10px 0;
        }

        @media (max-width: 768px) {
            .container {
                padding: 20px;
            }

            th, td {
                padding: 10px 15px;
                font-size: 0.9em;
            }

            h1 {
                font-size: 2em;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Сводная таблица</h1>
        <h2>Список учеников и их принадлежность к группам</h2>

        <div class="stats">
            <div class="stat-card">
                <div>Всего записей</div>
                <div class="stat-value" id="total-count">0</div>
            </div>
        </div>
""")

conn = sqlite3.connect('dances.db')
cursor = conn.cursor()

cursor.execute('''
    SELECT Dancers.name, Groups.dance_name
    FROM Dancers
    JOIN Participation ON Dancers.dancer_id = Participation.dancer_id
    JOIN Groups ON Participation.dance_id = Groups.dance_id
''')
results = cursor.fetchall()

print("""
        <table>
            <thead>
                <tr>
                    <th>Танцор</th>
                    <th>Группа</th>
                </tr>
            </thead>
            <tbody>
""")

for row in results:
    print(f"""
                <tr>
                    <td>{row[0]}</td>
                    <td>{row[1]}</td>
                </tr>
    """)

print("""
            </tbody>
        </table>

        <center>
            <a href="/cgi-bin/dance.py" class="back-btn">Вернуться на главную</a>
        </center>

        <script>
            // Обновляем счетчик записей
            document.getElementById('total-count').textContent = document.querySelectorAll('tbody tr').length;

            // Добавляем анимацию при загрузке
            document.addEventListener('DOMContentLoaded', function() {
                const rows = document.querySelectorAll('tbody tr');
                rows.forEach((row, index) => {
                    setTimeout(() => {
                        row.style.opacity = '1';
                    }, index * 50);
                });
            });
        </script>
    </div>
</body>
</html>
""")

conn.close()