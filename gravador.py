import csv
import os
import sqlite3


def gravador_bd(url_texto, url_id):
    if not os.path.exists('Database'):
        os.mkdir('Database')
    
    conn = sqlite3.connect('Database/coleta.db')
    cursor = conn.cursor()

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS links (
               id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
               url TEXT NOT NULL,
               status INTEGER NOT NULL,
               page_id TEXT NOT NULL
               );''')
    
    for link in url_texto:
        cursor.execute('''
            INSERT INTO links (url, status, page_id)
            VALUES (?, ?, ?);
            ''', (link, 0, url_id))
    conn.commit()
    

'''def gravador_txt(url_texto, nome):
    if not os.path.exists('Arquivos'):
        os.makedirs('Arquivos')
    
    for link in url_texto:
        with open('Arquivos\\{}_urls.txt'.format(nome), 'a', encoding="utf8") as arquivo:
            arquivo.writelines(link + '\n')'''
  

def gravador_csv(lista, nome):
    with open('Arquivos\\{}_detalhado.csv'.format(nome),
              'a', encoding='utf8', newline='') as arquivo_csv:
        gravador = csv.writer(arquivo_csv)
        file_is_empty = os.stat('Arquivos\\{}_detalhado.csv'.format(nome)).st_size == 0
        dados = ['titulo', 'texto', 'status', 'local', 'data',
                 'categoria_1', 'categoria_2', 'categoria_3',
                 'url_reclamacao']
        if file_is_empty:
            gravador.writerow(dados)
        for linha in lista:
            gravador.writerow(linha)
