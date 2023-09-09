import os
import sqlite3
import constants


def db_conn():
    if not os.path.exists('Database'):
        os.mkdir('Database')

    conn = sqlite3.connect('Database/coleta.db')
    cursor = conn.cursor()

    return conn, cursor


def db_writer(url_texto, url_id, conn, cursor):
    cursor.execute(constants.SQL_CREATE_TABLE)

    for link in url_texto:
        cursor.execute(constants.SQL_INSERT_LINK, (link, 0, url_id))
    conn.commit()

    with open('Arquivos/{}_log.txt'.format(url_id), 'a', encoding='utf8') as logfile:
        logfile.writelines('URL_ID:{}'.format(url_id))


def update_status(cursor, status, url, id_page):
    cursor.execute(constants.SQL_STATUS_UPDATE.format(
        status), (url, id_page))
