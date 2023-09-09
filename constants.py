COMPLAIN_LIST_BASE_URL = "https://www.reclameaqui.com.br/empresa/{}/lista-reclamacoes/?pagina=1"

COMPLAIN_URL_SELECTOR = "div.sc-1sm4sxr-0 a"
COMPLAIN_TEXT_SELECTOR = 'p[data-testid="complaint-description"]'
COMPLAIN_TITLE_SELECTOR = 'h1[data-testid="complaint-title"]'
COMPLAIN_LOCAL_SELECTOR = 'span[data-testid="complaint-location"]'
COMPLAIN_DATE_SELECTOR = 'span[data-testid="complaint-creation-date"]'
COMPLAIN_STATUS_SELECTOR = 'div[data-testid="complaint-status"]'

COMPLAIN_CATEGORY_1_SELECTOR = 'li[data-testid="listitem-categoria"]'
COMPLAIN_CATEGORY_2_SELECTOR = 'li[data-testid="listitem-produto"]'
COMPLAIN_CATEGORY_3_SELECTOR = 'li[data-testid="listitem-problema"]'

SQL_SELECT_URL = "SELECT DISTINCT url FROM links where status in(0) and page_id in(?)"
SQL_STATUS_UPDATE = "UPDATE links set status = {} where url = ? and page_id = ?;"
SQL_CREATE_TABLE = "CREATE TABLE IF NOT EXISTS links (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,url TEXT NOT NULL,status INTEGER NOT NULL,page_id TEXT NOT NULL);"
SQL_INSERT_LINK = "INSERT INTO links (url, status, page_id) VALUES (?, ?, ?);"
SQL_SUCCESS_STATUS = "1"
SQL_ERROR_STATUS = "3"

CSV_FILE_HEADERS = ['url', 'titulo', 'texto', 'status', 'local',
                    'data_hora', 'problem_type', 'product_type', 'category']
