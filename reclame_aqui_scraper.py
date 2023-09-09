from utils import define_browser, arguments
from database import db_conn
from scraper import scraper
from url_collector import url_collector


def main():
    args = arguments()
    driver = define_browser(args.browser)
    print('\n-- RECLAME AQUI SCRAPER --')
    conn, cursor = db_conn()
    coletor = url_collector(driver, args.file, args.id,
                            args.pages, conn, cursor)
    scraper(driver, coletor, args.id, conn, cursor)
    driver.quit()


if __name__ == '__main__':
    main()
