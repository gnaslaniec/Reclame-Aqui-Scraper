import logging
import datetime


logger = logging.getLogger(__name__)

logger.propagate = False

logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def write_log_file(id_page, url):
    with open('Arquivos/{}_log.txt'.format(id_page), 'a', encoding='utf8') as logfile:
        logfile.writelines('\n{} URL:{} OK'.format(
            datetime.datetime.now(), url))


def write_log_file_error(id_page, url, e):
    with open('Arquivos/{}_log.txt'.format(id_page), 'a', encoding='utf8') as logfile:
        logfile.writelines('\n{} URL:{} EXCEPTION {}'.format(
            datetime.datetime.now(), url, e))
