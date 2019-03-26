from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options


def driver_chrome():
    # Configurações para execução.
    chrome_options = Options()
    chrome_options.headless = True
    # Inicializa o webdriver.
    driver = webdriver.Chrome(options=chrome_options)

    return driver


def driver_firefox():
    # Configurações para execução.
    firefox_options = Options()
    firefox_options.headless = True
    # Inicializa o webdriver.
    driver = webdriver.Firefox(options=firefox_options)

    return driver
