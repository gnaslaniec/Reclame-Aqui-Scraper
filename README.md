# Reclame Aqui Scraper
Scraper escrito em Python para o site Reclame Aqui.

### Pré-requisitos

Os requisistos são o Python na versão 3+ , instalar a biblioteca Selenium, e o executável do Chromedriver ou Geckodriver.

```bash
$ pip install selenium
```
### Modo de uso

```bash
$ python reclame_aqui_scraper.py -i <ID da página> -p <Quantidade de páginas> -f <Nome do arquivo com os dados da coleta> -b <Browser para efetuar a coleta>
```
### Argumentos
<pre>
-i --id       Para verificar o ID da página basta ir até a URL da reclamação e copiar os números após o valor 'id': https://www.reclameaqui.com.br/indices/lista_reclamacoes/?id=<b>1111</b>&page=1&size=10&status=ALL

-p --pages    Número de páginas em que serão coletadas as reclamações. Ex.: '10' irá coletar reclamações da 10 primeiras páginas.

-f --file     Nome do arquivo em que será gravado os dados das reclamações.

-b --browser  Browser em que será efetuado a coleta, (F) para Firefox ou (C) para Chrome.
</pre>
