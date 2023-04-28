COMPLAIN_LIST_BASE_URL = "https://www.reclameaqui.com.br/empresa/{}/lista-reclamacoes/?pagina=1"

COMPLAIN_URL_SELECTOR = "div.sc-1sm4sxr-0 a"
COMPLAIN_TEXT_SELECTOR = ".lzlu7c-17"
COMPLAIN_TITLE_SELECTOR = ".lzlu7c-3"
COMPLAIN_LOCAL_SELECTOR = "div.lzlu7c-6:nth-child(1) > span:nth-child(2)"
COMPLAIN_DATE_SELECTOR = "div.lzlu7c-6:nth-child(2) > span:nth-child(2)"
COMPLAIN_STATUS_SELECTOR = "div.sc-1a60wwz-2:nth-child(1) > span:nth-child(2)"

COMPLAIN_CATEGORY_1_SELECTOR = ".lzlu7c-11 > ul:nth-child(1) > li:nth-child(1) > div:nth-child(1) > a:nth-child(1)"
COMPLAIN_CATEGORY_2_SELECTOR = ".lzlu7c-11 > ul:nth-child(1) > li:nth-child(2) > div:nth-child(1) > a:nth-child(1)"
COMPLAIN_CATEGORY_3_SELECTOR = ".lzlu7c-11 > ul:nth-child(1) > li:nth-child(3) > div:nth-child(1) > a:nth-child(1)"

SQL_SELECT_URL = "SELECT DISTINCT url FROM links where status in(0) and page_id in(?)"
SQL_STATUS_UPDATE = "UPDATE links set status = {} where url = ? and page_id = ?;"
SQL_CREATE_TABLE =  "CREATE TABLE IF NOT EXISTS links (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,url TEXT NOT NULL,status INTEGER NOT NULL,page_id TEXT NOT NULL);"
SQL_INSERT_LINK = "INSERT INTO links (url, status, page_id) VALUES (?, ?, ?);"

CSV_FILE_HEADERS = ['url','titulo', 'texto', 'status', 'local', 'data_hora', 'problem_type', 'product_type', 'category']