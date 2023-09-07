# Reclame Aqui Scraper
Scraper escrito em Python para o site Reclame Aqui, que permite coletar a URL, o conteúdo da reclamação, o status, a data e o local.

:warning: **AVISO**: O site do Reclame Aqui só permite visualizar reclamações até a página 50. Ou seja, não é possível acessar reclamações além desse ponto. Por favor, leve isso em consideração ao usar esse código para suas pesquisas ou avaliações. :warning:

### Pré-requisitos

Antes de usar este projeto, certifique-se de atender aos seguintes pré-requisitos:

- Python 3 ou versão posterior.
- Firefox ou Google Chrome em suas últimas versões.
- As bibliotecas Selenium e Webdriver Manager, que podem ser instaladas com o seguinte comando:

```bash
$ pip install selenium webdriver-manager
```

### Modo de uso

```bash
$ python reclame_aqui_scraper.py -i <ID da página> -p <Quantidade de páginas> -f <Nome do arquivo com os dados da coleta> -b <Browser para efetuar a coleta>
```

### Argumentos
<pre>
-i --id  Nome da página que se encontra na URL da empresa no ReclameAqui (por exemplo, "livraria-cultura", "spotify", "magazine-luiza-loja-online"). Insira o nome sem aspas.

-p --pages  Número de páginas das quais serão coletadas as reclamações (por exemplo, '10' para coletar reclamações das 10 primeiras páginas).

-f --file  Nome do arquivo no qual os dados das reclamações serão gravados.

-b --browser  Browser a ser utilizado para a coleta, use "F" ou "firefox" para Firefox, ou "C" ou "chrome" para Chrome.
</pre>
