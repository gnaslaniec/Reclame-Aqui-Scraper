import logging
import datetime


logger = logging.getLogger(__name__)

logger.propagate = False

logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def write_log_file(id_page, url, status='OK', e=None):
    with open('Arquivos/{}_log.txt'.format(id_page), 'a', encoding='utf8') as logfile:
        if status == 'OK':
            logfile.writelines('\n{} URL:{} OK'.format(
                datetime.datetime.now(), url))
        elif status == 'EXCEPTION' and e is not None:
            logfile.writelines('\n{} URL:{} EXCEPTION {}'.format(
                datetime.datetime.now(), url, e))
