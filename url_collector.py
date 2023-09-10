from logger import logger
from database import db_writer
from selenium.webdriver.common.by import By

import os
import constants
import re
import time


def url_collector(driver, file, id_page, pages, conn, cursor):
    create_file_folder()
    if log_file_exists(id_page):
        logger.info(
            'Já foram coletados os link para o ID: {}'.format(id_page))
        return file
    else:
        logger.info("ID: {}".format(file))

        url = constants.COMPLAIN_LIST_BASE_URL.format(id_page)
        cont = 1

        val = re.search(r'pagina=[0-9]+', url, re.MULTILINE)
        url = url.replace(val.group(0), 'pagina={}')
        lista_urls = []
        while cont <= int(pages):
            driver.get(url.format(cont))
            logger.info("Página {}".format(cont))
            time.sleep(5)
            url_pg = driver.find_elements(
                By.CSS_SELECTOR, constants.COMPLAIN_URL_SELECTOR)
            for u in url_pg:
                logger.info(u.get_attribute('href'))
                lista_urls.append(u.get_attribute('href'))

            logger.info("Página {} OK".format(cont))
            cont = cont + 1
        db_writer(lista_urls, id_page, conn, cursor)
        logger.info('Coleta de URLs concluída para o ID: {}'.format(file))
    return file


def create_file_folder():
    if not os.path.exists('Arquivos'):
        os.mkdir('Arquivos')


def log_file_exists(id_page):
    if os.path.exists('Arquivos/{}_log.txt'.format(id_page)):
        return True
    return False
