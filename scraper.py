import constants
from Reclamacao import Reclamacao
from database import gravador_bd, update_status
from utils import gravador_csv, format_url
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
logging.basicConfig(level=logging.INFO)


def url_collector(driver, file, id_page, pages, conn, cursor):
    create_file_folder()
    if log_file_exists(id_page):
        pass
    else:
        logging.info("ID: {}".format(file))

        url = constants.COMPLAIN_LIST_BASE_URL.format(id_page)
        cont = 1

        val = re.search(r'pagina=[0-9]+', url, re.MULTILINE)
        url = url.replace(val.group(0), 'pagina={}')
        lista_urls = []
        while cont <= int(pages):
            driver.get(url.format(cont))
            logging.info("Página {}".format(cont))
            time.sleep(5)
            url_pg = driver.find_elements(
                By.CSS_SELECTOR, constants.COMPLAIN_URL_SELECTOR)
            for u in url_pg:
                logging.info(u.get_attribute('href'))
                lista_urls.append(u.get_attribute('href'))

            logging.info("Página {} OK".format(cont))
            cont = cont + 1
        gravador_bd(lista_urls, id_page, conn, cursor)
        logging.info('Coleta de URLs concluída para o ID: {}'.format(file))

    return file


def scraper(driver, nome, id_page, conn, cursor):
    cursor.execute(constants.SQL_SELECT_URL, (id_page,))
    urls = cursor.fetchall()

    cont = 1
    for url in urls:
        try:
            url = format_url(url)
            driver.get(url)
            wait_page_load(driver)
            logging.info('Acessando: {}'.format(url[30:]))
            time.sleep(2)
            reclamacao = create_complaint(url, driver)
            gravador_csv(reclamacao.to_dict(), nome)
            logging.info('URL {} OK'.format(cont))
            cont = cont + 1
            update_status(cursor, constants.SQL_SUCCESS_STATUS,
                          url, id_page)
            conn.commit()
            write_log_file(id_page, url)
            time.sleep(2)
        except TimeoutException as e:
            logging.error(
                'Não foi possível acessar a reclamação, indo para próxima...\n')
            update_status(cursor, constants.SQL_ERROR_STATUS,
                          url, id_page)
            conn.commit()
            write_log_file_error(id_page, url, e)
            pass
        except WebDriverException as web_driver_exception:
            logging.error(web_driver_exception)
            driver.quit()
            conn.close()
            break

    logging.info('Coleta concluida! Nome do arquivo: {}'.format(nome))


def create_file_folder():
    if not os.path.exists('Arquivos'):
        os.mkdir('Arquivos')


def log_file_exists(id_page):
    if os.path.exists('Arquivos/{}_log.txt'.format(id_page)):
        logging.info(
            'Já foram coletados os link para o ID: {}'.format(id_page))
        return True
    return False


def write_log_file(id_page, url):
    with open('Arquivos/{}_log.txt'.format(id_page), 'a', encoding='utf8') as logfile:
        logfile.writelines('\n{} URL:{} OK'.format(
            datetime.datetime.now(), url))


def write_log_file_error(id_page, url, e):
    with open('Arquivos/{}_log.txt'.format(id_page), 'a', encoding='utf8') as logfile:
        logfile.writelines('\n{} URL:{} EXCEPTION {}'.format(
            datetime.datetime.now(), url, e))


def wait_page_load(driver):
    WebDriverWait(driver, 15).until(lambda x: x.find_element(
        By.CSS_SELECTOR, constants.COMPLAIN_TEXT_SELECTOR))


def create_complaint(url, driver):
    reclamacao = Reclamacao(
        url,
        driver.find_element(
            By.CSS_SELECTOR, constants.COMPLAIN_TEXT_SELECTOR).text,
        driver.find_element(
            By.CSS_SELECTOR, constants.COMPLAIN_TITLE_SELECTOR).text,
        driver.find_element(
            By.CSS_SELECTOR, constants.COMPLAIN_LOCAL_SELECTOR).text,
        driver.find_element(
            By.CSS_SELECTOR, constants.COMPLAIN_DATE_SELECTOR).text,
        driver.find_element(
            By.CSS_SELECTOR, constants.COMPLAIN_STATUS_SELECTOR).text
    )

    try:
        categoria1 = driver.find_element(
            By.CSS_SELECTOR, constants.COMPLAIN_CATEGORY_1_SELECTOR)
        reclamacao.problem_type = categoria1.text
    except NoSuchElementException:
        pass

    try:
        categoria2 = driver.find_element(
            By.CSS_SELECTOR, constants.COMPLAIN_CATEGORY_2_SELECTOR)
        reclamacao.product_type = categoria2.text
    except NoSuchElementException:
        pass

    try:
        categoria3 = driver.find_element(
            By.CSS_SELECTOR, constants.COMPLAIN_CATEGORY_3_SELECTOR)
        reclamacao.category = categoria3.text
    except NoSuchElementException:
        pass

    return reclamacao
