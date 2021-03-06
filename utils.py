from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options

import csv
import os
import sqlite3
import argparse

def arguments():
    parser = argparse.ArgumentParser('Reclame Aqui Scraper')
    parser.add_argument('-i', '--id', help='Link ou ID da empresa no Reclame Aqui', action='store', dest='id', required=True)
    parser.add_argument('-p', '--pages', help='Número de páginas para coletar', action='store', dest='pages', required=True)
    parser.add_argument('-f', '--file', help='Nome do arquivo em que será salvo os dados da coleta', action='store', dest='file', required=True)
    parser.add_argument('-b', '--browser', help='Browser que será utilizado para a coleta, (F) para Firefox e (C) para Chrome', 
                        action='store', dest='browser',required=True)
    
    args = parser.parse_args()

    return args

''' Driver Selenium com Chrome '''
def driver_chrome():
    # Configurações para execução.
    chrome_options = Options()
    chrome_options.headless = True
    # Inicializa o webdriver.
    driver = webdriver.Chrome(options=chrome_options, executable_path="Drivers\\chromedriver.exe")

    return driver


''' Driver Selenium com Firefox '''
def driver_firefox():
    # Configurações para execução.
    firefox_options = Options()
    firefox_options.headless = True
    # Inicializa o webdriver.
    driver = webdriver.Firefox(options=firefox_options, executable_path="Drivers\\geckodriver.exe")

    return driver


''' Função para inicialização do banco de dados '''
def db_conn():
    if not os.path.exists('Database'):
        os.mkdir('Database')
    
    conn = sqlite3.connect('Database/coleta.db')
    cursor = conn.cursor()

    return conn, cursor

''' Função para gravar os links no banco de dados '''
def gravador_bd(url_texto, url_id, conn, cursor):
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

    with open('Arquivos/{}_log.txt'.format(url_id), 'a', encoding='utf8') as logfile:
        logfile.writelines('URL_ID:{}'.format(url_id))
    

''' Função para gravar os detalhes das reclamações em um arquivo CSV '''
def gravador_csv(lista, nome):
    with open('Arquivos\\{}.csv'.format(nome),
              'a', encoding='utf8', newline='') as arquivo_csv:
        gravador = csv.writer(arquivo_csv)
        file_is_empty = os.stat('Arquivos\\{}.csv'.format(nome)).st_size == 0
        dados = ['titulo', 'texto', 'status', 'local', 'data',
                 'categoria_1', 'categoria_2', 'categoria_3',
                 'url_reclamacao']
        if file_is_empty:
            gravador.writerow(dados)
        for linha in lista:
            gravador.writerow(linha)


# Arredondamentos para o horário
def arrendonda_hora(hora):
    """ VARIÁVEIS PARA TRATAMENTOS DO HORÁRIO! """
    # Arredonda pra 00
    grupo_1 = {'00', '01', '02', '03', '04', '05', '06',
            '07', '08', '09', '10', '11', '12',
            '13', '14', '15', '16', '17', '18',
            '19', '20', '21', '22', '23', '24',
            '25', '56', '57', '58', '59'}

    # Verifica se será alterado o valor inicial
    grupo_aumenta = {'56', '57', '58', '59'}

    # Arredonda pra 30
    grupo_2 = {'26', '27', '28', '29', '30', '31', '32', '33',
            '34', '35', '36', '37', '38', '39', '40', '41',
            '42', '43', '44', '45', '46', '47', '48', '49',
            '50', '51', '52', '53', '54', '55'}

    if hora[-2:] in grupo_1:
        if hora[-2:] in grupo_aumenta:
            if hora[-5:-3] != '23':
                valor_novo = int(hora[-5:-3]) + 1
                hora = hora.replace(hora[-5:-3], str(valor_novo))
                hora = hora[:-2] + '00'
            else:
                valor_novo = '00'
                hora = hora.replace(hora[-5:-3], valor_novo)
                hora = hora[:-2] + '00'
        else:
            hora = hora[:-2] + '00'
    # Arredonda pra 30
    elif hora[-2:] in grupo_2:
        hora = hora[:-2] + '30'
    else:
        print('Horário inválido!')

    return hora
