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

from utils import gravador_csv, gravador_bd, format_url
from Reclamacao import Reclamacao
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
                url_formated = format_url(url)
                driver.get(url_formated)
                WebDriverWait(driver, 15).until(lambda x: x.find_element(By.CSS_SELECTOR, constants.COMPLAIN_TEXT_SELECTOR))
                logging.info('Acessando: {}'.format(url_formated[30:]))
                time.sleep(2)
                
                reclamacao = Reclamacao(
                    url_formated,
                    driver.find_element(By.CSS_SELECTOR, constants.COMPLAIN_TEXT_SELECTOR).text,
                    driver.find_element(By.CSS_SELECTOR, constants.COMPLAIN_TITLE_SELECTOR).text,
                    driver.find_element(By.CSS_SELECTOR, constants.COMPLAIN_LOCAL_SELECTOR).text,
                    driver.find_element(By.CSS_SELECTOR, constants.COMPLAIN_DATE_SELECTOR).text,
                    driver.find_element(By.CSS_SELECTOR, constants.COMPLAIN_STATUS_SELECTOR).text
                )
                
                try:
                    categoria1 = driver.find_element(By.CSS_SELECTOR, constants.COMPLAIN_CATEGORY_1_SELECTOR)
                    reclamacao.problem_type = categoria1.text
                except NoSuchElementException:
                    pass

                try:
                    categoria2 = driver.find_element(By.CSS_SELECTOR, constants.COMPLAIN_CATEGORY_2_SELECTOR)
                    reclamacao.product_type = categoria2.text
                except NoSuchElementException:
                    pass

                try:
                    categoria3 = driver.find_element(By.CSS_SELECTOR, constants.COMPLAIN_CATEGORY_3_SELECTOR)
                    reclamacao.category = categoria3.text
                except NoSuchElementException:
                    pass

                gravador_csv(reclamacao.to_dict(), nome)

                logging.info('URL {} OK'.format(cont))
                cont = cont + 1
                cursor.execute(constants.SQL_STATUS_UPDATE.format('1'), (url_formated, id_page))
                conn.commit()
                with open('Arquivos/{}_log.txt'.format(id_page), 'a', encoding='utf8') as logfile:
                    logfile.writelines('\n{} URL:{} OK'.format(datetime.datetime.now(), url_formated))
                time.sleep(2)
            except TimeoutException as e:
                logging.error('Não foi possível acessar a reclamação, indo para próxima...\n')
                cursor.execute(constants.SQL_STATUS_UPDATE.format('3'), (url_formated,id_page))
                conn.commit()
                with open('Arquivos/{}_log.txt'.format(id_page), 'a', encoding='utf8') as logfile:
                    logfile.writelines('\n{} URL:{} EXCEPTION {}'.format(datetime.datetime.now(), url_formated, e))
                pass
            except WebDriverException as web_driver_exception:
                logging.error(web_driver_exception)
                driver.quit()
                conn.close()
                break
    
    logging.info('Coleta concluida! Nome do arquivo: {}'.format(nome))