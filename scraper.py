from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException

import time
import os
import re
import sqlite3
import datetime

from editor_tempo import arrendonda_hora
from gravador import gravador_csv, gravador_bd, db_conn

url_base = 'https://www.reclameaqui.com.br/empresa/{}/lista-reclamacoes/?pagina=1'


def url_collector(driver, file, id_page, pages, conn, cursor):
    nome = file
    if not os.path.exists('Arquivos'):
        os.mkdir('Arquivos')
    if os.path.exists('Arquivos/{}_log.txt'.format(id_page)):
        print('Já foram coletados os link para o ID: {}'.format(id_page))
        pass
    else:
        print('\n', nome, '\n')

        url_id = id_page
        pgs = int(pages)
        url = url_base.format(url_id)
        cont = 1
        
        val = re.search(r'pagina=[0-9]+', url, re.MULTILINE)
        url = url.replace(val.group(0), 'pagina={}')
        url_texto = []
        while cont <= pgs:
            driver.get(url.format(cont))
            print("\nPágina {}".format(cont))
            time.sleep(5)
            #url_pg = driver.find_elements_by_xpath("//div[@class='link-complain-id-complains']")
            url_pg = driver.find_elements_by_css_selector("a.link-complain-id-complains")
            print('\nurl')
            for u in url_pg:
                print(u.get_attribute('href'))
                url_texto.append(u.get_attribute('href'))
                
            print("\n\nColetados os links da Página {}!!!".format(cont))
            cont = cont + 1
        gravador_bd(url_texto, url_id, conn, cursor)
        print('Coleta dos links concluídos para a página {}'.format(nome))

    return nome


def scraper(driver, nome, id_page, conn, cursor):
    sql = '''SELECT DISTINCT url
        FROM links where status in(0) 
        and page_id in(?);'''

    sql_status = 'UPDATE links set status = {} where url = ? and page_id = ?;'
        
    cursor.execute(sql, (id_page,))
    urls = cursor.fetchall()
    
    cont = 1    
    for url in urls:
            try:
                url_str = str(url)
                url = url_str.replace("(", "").replace(")", "").replace("'", "").replace(",", "")
                driver.get(url)
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
                cursor.execute(sql_status.format('1'), (url,id_page))
                conn.commit()
                with open('Arquivos/{}_log.txt'.format(id_page), 'a', encoding='utf8') as logfile:
                    logfile.writelines('\n{} URL:{} OK'.format(datetime.datetime.now(), url))
                time.sleep(2)
            except TimeoutException as e:
                print('Não foi possível acessar a reclamação, indo para próxima...\n')
                cursor.execute(sql_status.format('3'), (url,id_page))
                conn.commit()
                with open('Arquivos/{}_log.txt'.format(id_page), 'a', encoding='utf8') as logfile:
                    logfile.writelines('\n{} URL:{} EXCEPTION {}'.format(datetime.datetime.now(), url, e))
                pass
            except WebDriverException as web_driver_exception:
                print('Foi perdida a conexão!')
                driver.quit()
                conn.close()
                break
    
    print('Coleta concluida! Nome do arquivo: {}_detalhado'.format(nome))
        
