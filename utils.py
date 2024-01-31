from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

import csv
import os
import argparse

import constants


def arguments():
    parser = argparse.ArgumentParser('Reclame Aqui Scraper')
    parser.add_argument('-i', '--id', help='Link ou ID da empresa no Reclame Aqui',
                        action='store', dest='id', required=True)
    parser.add_argument('-p', '--pages', help='Número de páginas para coletar',
                        action='store', dest='pages', required=True, type=int)
    parser.add_argument('-f', '--file', help='Nome do arquivo em que será salvo os dados da coleta',
                        action='store', dest='file', required=True)
    parser.add_argument('-b', '--browser', help='Browser que será utilizado para a coleta, (F) para Firefox e (C) para Chrome',
                        action='store', dest='browser', nargs='?', default="f")
    args = parser.parse_args()
    return args


def driver_chrome():
    chrome_options = Options()
    chrome_options.headless = True
    service =Service(executable_path=GeckoDriverManager(
    ).install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def driver_firefox():
    firefox_options = Options()
    firefox_options.headless = True
    # service = Service(executable_path='./chromedriver.exe')
    service = Service(executable_path=GeckoDriverManager(
    ).install())
    driver = webdriver.Firefox(service=service, options=firefox_options)
    return driver


def define_browser(argument):
    if (argument.lower() == "c" or argument.lower() == "chrome"):
        return driver_chrome()
    if (argument.lower() == "f" or argument.lower() == "firefox"):
        return driver_firefox()
    raise Exception("Invalid browser argument.")


def csv_writer(reclamacao, nome):
    with open('Arquivos/{}.csv'.format(nome),
              'a', encoding='utf8', newline='') as arquivo_csv:
        writer = csv.DictWriter(
            arquivo_csv, fieldnames=constants.CSV_FILE_HEADERS)
        file_is_empty = os.stat('Arquivos//{}.csv'.format(nome)).st_size == 0
        if file_is_empty:
            writer.writeheader()
        writer.writerow(reclamacao)


def format_url(url):
    url_str = str(url)
    return url_str.replace("(", "").replace(")", "").replace("'", "").replace(",", "")
