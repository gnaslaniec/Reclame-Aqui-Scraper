# Reclame Aqui Scraper
Scraper escrito em Python para o site Reclame Aqui, que permite coletar a url, a reclamação em si, o status, data e local.

### Pré-requisitos

Os requisistos são o Python na versão 3+ , Firefox ou Google Chrome em suas últimas versões, e instalar a biblioteca Selenium com o seguinte comando:

```bash
$ pip install selenium
```
### Modo de uso

```bash
$ python reclame_aqui_scraper.py -i <ID da página> -p <Quantidade de páginas> -f <Nome do arquivo com os dados da coleta> -b <Browser para efetuar a coleta>
```
### Argumentos
<pre>
-i --id       Nome da página que se encontra na url da empresa no ReclameAqui. Ex.: "livraria-cultura" , "spotify", "magazine-luiza-loja-online" (inserir o nome sem aspas)

-p --pages    Número de páginas em que serão coletadas as reclamações. Ex.: '10' irá coletar reclamações da 10 primeiras páginas.

-f --file     Nome do arquivo em que será gravado os dados das reclamações.

-b --browser  Browser em que será efetuado a coleta, (F) para Firefox ou (C) para Chrome.
</pre>
