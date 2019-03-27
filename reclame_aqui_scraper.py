from selenium_driver import driver_chrome, driver_firefox
from scraper import url_collector, scraper
from arguments import arguments


def main():
    args = arguments()
    browser = args.browser
    if browser.lower() == 'c' or browser.lower() == 'chrome':
        driver = driver_chrome()
    elif browser.lower() == 'f' or browser.lower() == 'firefox':
        driver = driver_firefox()
    print('-- RECLAME AQUI SCRAPER --')
    
    file = args.file
    id_page = args.id
    pages = args.pages

    
    
    coletor = url_collector(driver, file, id_page, pages, file_type)
    scraper(driver, coletor, id_page)
    driver.quit()


if __name__ == '__main__':
    main()
