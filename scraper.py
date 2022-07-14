from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

import time
import os
import re
import datetime
import logging
logging.basicConfig(level = logging.INFO)

from utils import gravador_csv, gravador_bd, arrendonda_hora
import constants

def url_collector(driver, file, id_page, pages, conn, cursor):
    nome = file
    if not os.path.exists('Arquivos'):
        os.mkdir('Arquivos')
    if os.path.exists('Arquivos/{}_log.txt'.format(id_page)):
        logging.info('Já foram coletados os link para o ID: {}'.format(id_page))
        pass
    else:
        logging.info("ID: {}".format(nome))

        url_id = id_page
        numero_paginas = int(pages)
        url = constants.COMPLAIN_LIST_BASE_URL.format(url_id)
        cont = 1
        
        val = re.search(r'pagina=[0-9]+', url, re.MULTILINE)
        url = url.replace(val.group(0), 'pagina={}')
        lista_urls = []
        while cont <= numero_paginas:
            driver.get(url.format(cont))
            logging.info("Página {}".format(cont))
            time.sleep(5)
            url_pg = driver.find_elements(By.CSS_SELECTOR, constants.COMPLAIN_URL_SELECTOR)
            for u in url_pg:
                logging.info(u.get_attribute('href'))
                lista_urls.append(u.get_attribute('href'))
                
            logging.info("Página {} OK".format(cont))
            cont = cont + 1
        gravador_bd(lista_urls, url_id, conn, cursor)
        logging.info('Coleta de URLs concluída para o ID: {}'.format(nome))

    return nome


def scraper(driver, nome, id_page, conn, cursor):
    cursor.execute(constants.SQL_SELECT_URL, (id_page,))
    urls = cursor.fetchall()
    
    cont = 1    
    for url in urls:
            try:
                url_str = str(url)
                url = url_str.replace("(", "").replace(")", "").replace("'", "").replace(",", "")
                driver.get(url)
                WebDriverWait(driver, 15).until(lambda x: x.find_element(By.CSS_SELECTOR,'.lzlu7c-17'))
                logging.info('Acessando: {}'.format(url[30:]))
                time.sleep(2)

                texto = driver.find_element(By.CSS_SELECTOR, constants.COMPLAIN_TEXT_SELECTOR)
                titulo = driver.find_element(By.CSS_SELECTOR, constants.COMPLAIN_TITLE_SELECTOR)
                local = driver.find_element(By.CSS_SELECTOR, constants.COMPLAIN_LOCAL_SELECTOR)
                data_hora = driver.find_element(By.CSS_SELECTOR, constants.COMPLAIN_DATE_SELECTOR)
                status = driver.find_element(By.CSS_SELECTOR, constants.COMPLAIN_STATUS_SELECTOR)

                try:
                    categoria1 = driver.find_element(By.CSS_SELECTOR, constants.COMPLAIN_CATEGORY_1_SELECTOR)
                    problem_type = categoria1.text
                except NoSuchElementException:
                    problem_type = '--'

                try:
                    categoria2 = driver.find_element(By.CSS_SELECTOR, constants.COMPLAIN_CATEGORY_2_SELECTOR)
                    product_type = categoria2.text
                except NoSuchElementException:
                    product_type = '--'

                try:
                    categoria3 = driver.find_element(By.CSS_SELECTOR, constants.COMPLAIN_CATEGORY_3_SELECTOR)
                    category = categoria3.text
                except NoSuchElementException:
                    category = '--'

                hora = data_hora.text
                hora = arrendonda_hora(hora)

                lista = zip([titulo.text], [texto.text],
                            [status.text], [local.text],
                            [hora], [problem_type],
                            [product_type], [category], [url])

                gravador_csv(lista, nome)

                logging.info('URL {} OK'.format(cont))
                cont = cont + 1
                cursor.execute(constants.SQL_STATUS_UPDATE.format('1'), (url,id_page))
                conn.commit()
                with open('Arquivos/{}_log.txt'.format(id_page), 'a', encoding='utf8') as logfile:
                    logfile.writelines('\n{} URL:{} OK'.format(datetime.datetime.now(), url))
                time.sleep(2)
            except TimeoutException as e:
                logging.error('Não foi possível acessar a reclamação, indo para próxima...\n')
                cursor.execute(constants.SQL_STATUS_UPDATE.format('3'), (url,id_page))
                conn.commit()
                with open('Arquivos/{}_log.txt'.format(id_page), 'a', encoding='utf8') as logfile:
                    logfile.writelines('\n{} URL:{} EXCEPTION {}'.format(datetime.datetime.now(), url, e))
                pass
            except WebDriverException as web_driver_exception:
                logging.error(web_driver_exception)
                driver.quit()
                conn.close()
                break
    
    logging.info('Coleta concluida! Nome do arquivo: {}'.format(nome))
