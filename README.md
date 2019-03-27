# Reclame-Aqui-Scraper
Scraper escrito em Python para o site Reclame Aqui.

### Prerequisites

Os únicos requisistos são o Python na versão 3+ e instalar a biblioteca Selenium.

```bash
$ pip install selenium
```
### Modo de uso

```bash
$ python reclame_aqui_scraper.py -i <ID da página> -p <Quantidade de páginas> -f <Nome do arquivo com os dados da coleta> -b <Browser para efetuar a coleta>
```
Para verificar o ID da página basta ir até a URL da reclamação e copiar os números após o valor 'id':
<pre>
https://www.reclameaqui.com.br/indices/lista_reclamacoes/?id=<b>1111</b>&page=1&size=10&status=ALL
</pre>
