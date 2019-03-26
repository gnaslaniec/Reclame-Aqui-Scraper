from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

import time
import os
import re
import sqlite3

from editor_tempo import arrendonda_hora
from gravador import gravador_csv, gravador_txt, gravador_bd

url_base = 'https://www.reclameaqui.com.br/indices/lista_reclamacoes/?id={}&size=10&page=1&status=ALL'


def url_collector(driver, file, id_page, pages):
    nome = file
    if not os.path.exists('Arquivos'):
        os.mkdir('Arquivos')
    if os.path.exists('Arquivos/{}_urls.txt'.format(nome)):
        print('Arquivo com os links já existe!')
        pass
    else:
        print('\n', nome, '\n')

        url_id = id_page
        pgs = int(pages)
        if str.isdigit(url_id):
            url = url_base.format(url_id)
        else:
            url = url_id

        cont = 1
        
        val = re.search(r'page=[0-9]+', url, re.MULTILINE)
        url = url.replace(val.group(0), 'page={}')
        url_texto = []
        while cont <= pgs:
            driver.get(url.format(cont))
            print("\nPágina {}".format(cont))
            time.sleep(5)
            url_pg = driver.find_elements_by_xpath("//div[@class='complain-status-title']/a")
            print('\nurl')
            for u in url_pg:
                print(u.get_attribute('href'))
                url_texto.append(u.get_attribute('href'))
                
            print("\n\nColetados os links da Página {}!!!".format(cont))
            cont = cont + 1
        gravador_bd(url_texto, url_id)
        print('Coleta dos links concluídos para a página {}'.format(nome))

    return nome


def scraper(driver, nome, id_page):
    '''with open('Arquivos\\{}_urls.txt'.format(nome)) as arquivo_urls:
            valores = arquivo_urls.read()
            urls = valores.split()'''
  
    conn = sqlite3.connect('Database/coleta.db')
    cursor = conn.cursor()
        
    sql = '''SELECT DISTINCT url
        FROM links where status in(0) 
        and page_id in(?);'''
        
    cursor.execute(sql, (id_page,))
    urls = cursor.fetchall()
    
    cont = 1    
    for url in urls:
            try:
                url_str = str(url)
                url = url_str.replace("(", "").replace(")", "").replace("'", "").replace(",", "")
                driver.get(str(url))
                WebDriverWait(driver, 15).until(
                    lambda x: x.find_element_by_xpath('//*[@id="complain-detail"]'
                                                      '/div/div[1]/div[2]/div/div[1]'
                                                      '/div[2]/div[1]/ul[1]/li[1]'))
                print('Acessando: {}'.format(url[30:]))
                time.sleep(2)

                print('Iniciando!')

                texto = driver.find_element_by_xpath('//*[@id="complain-detail"]'
                                                     '/div/div[1]/div[2]/div/div[2]/p')
                titulo = driver.find_element_by_xpath('//*[@id="complain-detail"]'
                                                      '/div/div[1]/div[2]/div/div[1]/div[2]/div[1]/h1')
                local = driver.find_element_by_xpath('//*[@id="complain-detail"]'
                                                     '/div/div[1]/div[2]/div/div[1]/div[2]/div[1]/ul[1]/li[1]')
                data_hora = driver.find_element_by_xpath('//*[@id="complain-detail"]'
                                                         '/div/div[1]/div[2]/div/div[1]/div[2]/div[1]/ul[1]/li[3]')
                status = driver.find_element_by_xpath(
                    '/html/body/ui-view/div[3]/div/div/div[2]/div/div[1]/div[2]/div[2]/div/span/img')

                try:
                    categoria1 = driver.find_element_by_xpath(
                        '//*[@id="complain-detail"]/div/div[1]/div[2]/div/div[1]/div[2]/div[1]/ul[2]/li[1]')
                    problem_type = categoria1.text
                except NoSuchElementException:
                    problem_type = '--'

                try:
                    categoria2 = driver.find_element_by_xpath(
                        '//*[@id="complain-detail"]/div/div[1]/div[2]/div/div[1]/div[2]/div[1]/ul[2]/li[2]')
                    product_type = categoria2.text
                except NoSuchElementException:
                    product_type = '--'

                try:
                    categoria3 = driver.find_element_by_xpath(
                        '//*[@id="complain-detail"]/div/div[1]/div[2]/div/div[1]/div[2]/div[1]/ul[2]/li[3]')
                    category = categoria3.text
                except NoSuchElementException:
                    category = '--'

                hora = data_hora.text
                hora = arrendonda_hora(hora)

                print('Titulo: {}'.format(titulo.text))
                # print('Texto: {}'.format(texto.text))
                # print(local.text)
                # print(data.text)
                # print(status.text)
                # print('\n')

                lista = zip([titulo.text], [texto.text],
                            [status.get_attribute("title")], [local.text],
                            [hora], [problem_type],
                            [product_type], [category], [url])

                gravador_csv(lista, nome)

                print('URL {} OK'.format(cont), '\n')
                
                cont = cont + 1
                sql_status = 'UPDATE links set status = 1 where url = ? and page_id = ?;'
                cursor.execute(sql_status, (url,id_page))
                conn.commit()
                time.sleep(2)
            except TimeoutException:
                print('Não foi possível acessar a reclamação, indo para próxima...\n')
                sql_status = 'UPDATE links set status = 3 where url = ? and page_id = ?;'
                cursor.execute(sql_status, (url,id_page))
                conn.commit()
                pass

    print('Coleta concluida! Nome do arquivo: {}_detalhado'.format(nome))
    conn.close()
