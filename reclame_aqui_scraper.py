from utils import driver_chrome, driver_firefox, arguments, db_conn
from scraper import url_collector, scraper

def main():
    args = arguments()
    browser = args.browser
    if browser.lower() == 'c' or browser.lower() == 'chrome':
        driver = driver_chrome()
    elif browser.lower() == 'f' or browser.lower() == 'firefox':
        driver = driver_firefox()
    print('\n-- RECLAME AQUI SCRAPER --')
    
    file = args.file
    id_page = args.id
    pages = args.pages

    conn, cursor = db_conn()

    coletor = url_collector(driver, file, id_page, pages, conn, cursor)
    scraper(driver, coletor, id_page, conn, cursor)
    driver.quit()


if __name__ == '__main__':
    main()
