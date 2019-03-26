import sqlite3
import os

if not os.path.exists('Database'):
    os.mkdir('Database')

conn = sqlite3.connect('Database/teste.db')

cursor = conn.cursor()

cursor.execute('''
            CREATE TABLE IF NOT EXISTS links (
               id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
               url TEXT NOT NULL,
               status INTEGER NOT NULL
               );''')

print('Tabela Criada')

cursor.execute('''
            INSERT INTO links (url, status)
            VALUES ('https://www.reclameaqui.com.br/mercedes-benz/mercedes-415_keexNaD29alUCgNU/', 0)
''')


conn.commit()

cursor.execute("""
SELECT * FROM links;
""")

for linha in cursor.fetchall():
    print(linha)

conn.close()