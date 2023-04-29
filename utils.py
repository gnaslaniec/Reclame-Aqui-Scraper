from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options

import csv
import os
import argparse

import constants


def arguments():
    parser = argparse.ArgumentParser('Reclame Aqui Scraper')
    parser.add_argument('-i', '--id', help='Link ou ID da empresa no Reclame Aqui',
                        action='store', dest='id', required=True)
    parser.add_argument('-p', '--pages', help='Número de páginas para coletar',
                        action='store', dest='pages', required=True)
    parser.add_argument('-f', '--file', help='Nome do arquivo em que será salvo os dados da coleta',
                        action='store', dest='file', required=True)
    parser.add_argument('-b', '--browser', help='Browser que será utilizado para a coleta, (F) para Firefox e (C) para Chrome',
                        action='store', dest='browser', nargs='?', default="f")
    args = parser.parse_args()
    return args


def driver_chrome():
    chrome_options = Options()
    chrome_options.headless = True
    driver = webdriver.Chrome(options=chrome_options, executable_path=ChromeDriverManager(
    ).install(), service_log_path=None)
    return driver


def driver_firefox():
    firefox_options = Options()
    firefox_options.headless = True
    driver = webdriver.Firefox(options=firefox_options, executable_path=GeckoDriverManager()
                               .install(), service_log_path=None)
    return driver


def define_browser(argument):
    if (argument.lower() == "c" or argument.lower() == "chrome"):
        return driver_chrome()
    return driver_firefox()


def gravador_csv(reclamacao, nome):
    with open('Arquivos/{}.csv'.format(nome),
              'a', encoding='utf8', newline='') as arquivo_csv:
        gravador = csv.DictWriter(
            arquivo_csv, fieldnames=constants.CSV_FILE_HEADERS)
        file_is_empty = os.stat('Arquivos//{}.csv'.format(nome)).st_size == 0
        if file_is_empty:
            gravador.writeheader()
        gravador.writerow(reclamacao)


def format_url(url):
    url_str = str(url)
    return url_str.replace("(", "").replace(")", "").replace("'", "").replace(",", "")
