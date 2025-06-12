import sqlite3
import cgi
import sys

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)
print("Content-Type: text/html; charset=utf-8\n")
print("""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Студия танца I'm Dance Home</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            margin: 0;
            padding: 0;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            color: #333;
        }

        .container {
            background-color: white;
            border-radius: 15px;
            box-shadow: 0 10px 10px rgba(0, 0, 0, 0.1);
            padding: 40px;
            width: 80%;
            max-width: 600px;
            text-align: center;
        }

        h1 {
            color: #6a1b9a;
            margin-bottom: 40px;
            font-size: 2.5em;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.1);
        }

        .btn-container {
            display: flex;
            flex-direction: column;
            gap: 20px;
            margin-top: 30px;
        }

        .btn {
            background: linear-gradient(45deg, #9c4dcc, #6a1b9a);
            color: white;
            border: none;
            padding: 15px 0px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 15px;
            font-weight: 500;
            border-radius: 50px;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(106, 27, 154, 0.3);
            width: 100%;
        }

        .btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 7px 20px rgba(106, 27, 154, 0.4);
            background: linear-gradient(45deg, #6a1b9a, #9c4dcc);
        }

        .logo {
            width: 120px;
            height: 120px;
            background-color: #6a1b9a;
            border-radius: 50%;
            margin: 0 auto 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 24px;
            font-weight: bold;
            box-shadow: 0 5px 15px rgba(106, 27, 154, 0.3);
        }

        @media (max-width: 768px) {
            .container {
                width: 90%;
                padding: 30px 20px;
            }

            h1 {
                font-size: 2em;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">IDH</div>
        <h1>Студия танца I'm Dance Home</h1>

        <div class="btn-container">
            <a href='/cgi-bin/dancers.py' class='btn'>Просмотреть список учеников</a>
            <a href='/cgi-bin/other_table.py' class='btn'>Открыть сводную таблицу</a>
        </div>
    </div>
</body>
</html>
""")

