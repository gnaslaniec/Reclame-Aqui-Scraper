import argparse

def arguments():
    parser = argparse.ArgumentParser('Reclame Aqui Scraper')
    parser.add_argument('-i', '--id', help='Link ou ID da empresa no Reclame Aqui', action='store', dest='id', required=True)
    parser.add_argument('-p', '--pages', help='Número de páginas para coletar', action='store', dest='pages', required=True)
    parser.add_argument('-f', '--file', help='Nome do arquivo em que será salvo os dados da coleta', action='store', dest='file', required=True)
    parser.add_argument('-b', '--browser', help='Browser que será utilizado para a coleta, (F) para Firefox e (C) para Chrome', 
                        action='store', dest='browser',required=True)
    
    args = parser.parse_args()

    return args