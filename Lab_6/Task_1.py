import sqlite3


conn = sqlite3.connect('dances.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Dancers (
    dancer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Groups (
    dance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    dance_name TEXT NOT NULL,
    difficulty_level TEXT,
    count_person INTEGER
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Participation (
    participation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    dancer_id INTEGER,
    dance_id INTEGER,
    FOREIGN KEY (dancer_id) REFERENCES Dancers(dancer_id),
    FOREIGN KEY (dance_id) REFERENCES Dances(dance_id)
);
''')

cursor.execute("INSERT INTO Dancers (name, age) VALUES ('София Ковалева', '20')")
cursor.execute("INSERT INTO Dancers (name, age) VALUES ('Анна Иванова', '22')")
cursor.execute("INSERT INTO Dancers (name, age) VALUES ('Ольга Мотренко', '19')")
cursor.execute("INSERT INTO Dancers (name, age) VALUES ('Егор Сороров', '25')")
cursor.execute("INSERT INTO Dancers (name, age) VALUES ('Кристина Бабаян', '21')")

cursor.execute("INSERT INTO Groups (dance_name, difficulty_level, count_person) VALUES ('Hip-hop', 'beginner', 10)")
cursor.execute("INSERT INTO Groups (dance_name, difficulty_level, count_person) VALUES ('Juzz-funk', 'pro', 12)")
cursor.execute("INSERT INTO Groups (dance_name, difficulty_level, count_person) VALUES ('High heels', 'beginner', 10)")

cursor.execute("INSERT INTO Participation (dancer_id, dance_id) VALUES (1, 1)")
cursor.execute("INSERT INTO Participation (dancer_id, dance_id) VALUES (2, 2)")
cursor.execute("INSERT INTO Participation (dancer_id, dance_id) VALUES (3, 3)")
cursor.execute("INSERT INTO Participation (dancer_id, dance_id) VALUES (1, 3)")
cursor.execute("INSERT INTO Participation (dancer_id, dance_id) VALUES (4, 2)")
cursor.execute("INSERT INTO Participation (dancer_id, dance_id) VALUES (5, 1)")
cursor.execute("INSERT INTO Participation (dancer_id, dance_id) VALUES (5, 3)")
cursor.execute("INSERT INTO Participation (dancer_id, dance_id) VALUES (4, 1)")

cursor.execute('SELECT * FROM Dancers')
all_user = cursor.fetchall()

print("Все танцоры:")
for row in all_user:
  print(row)

cursor.execute('SELECT name FROM Dancers WHERE age > ?', (21,))
f1_user = cursor.fetchall()

print("Все танцоры, чей возраст больше 21:")
for row in f1_user:
  print(row)

cursor.execute('SELECT dance_name, count_person FROM Groups ORDER BY count_person')
sorted_group = cursor.fetchall()

print("Все группы, отсортированные по максимальному колличествоу человек: ")
for row in sorted_group:
  print(row[0])

cursor.execute('SELECT COUNT(*) FROM Dancers')
total_dancers = cursor.fetchone()[0]

print('Общее количество пользователей:', total_dancers)

conn.commit()
conn.close()

