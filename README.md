# Pig Batch Management API 🐖

Este repositório contêm um projeto da API de gerenciamento de lotes de leitões.

## Sumário 📄

* [Rodando localmente sem o uso do Docker](#rodando-localmente-sem-o-uso-do-docker)
* [Rodando localmente com o uso do Docker (via Docker Compose) 🐋](#rodando-localmente-com-o-uso-do-docker-via-docker-compose)

## Rodando localmente sem o uso do Docker

Para rodar este projeto localmente você precisará ter instalado em sua máquina:
1. [Python](https://www.python.org/downloads/) | versão 3.10, ou acima.
2. [Redis](https://redis.io/docs/latest/get-started/) | Para cache, criação e gerênciamento da fila de criação assíncrona dos lotes. (opite pelas versões mais recentes)
3. [PostgreSQL](https://www.postgresql.org/download/) | SGBD para criação e gerênciamento da base de dados (opite pelas versões mais recentes)

Após instalar as ferramentas acima, execute os seguintes passos:

1. Faça o clone do repositório [pig-batch-management-api](https://github.com/marcosalvesdev/pig-batch-management-api) 🐖
2. Instale as dependências: `pip install -r requirements.txt`
    ### Atenção ⚠️
    ### É altamente recomendado que você esteja em um ambiente isolado na sua máquina antes de executar o comando acima, se não souber como criar um aqui está um [tutorial](https://dev.to/franciscojdsjr/guia-completo-para-usar-o-virtual-environment-venv-no-python-57bo) de como fazer.
3. Crie um arquivo `.env` (use o arquivo `.env.example` como referência) com as seguintes vari veis de ambiente:
    - Caso você não use um arquivo `.env` os valores defaults deixados no arquivo de configuração (settings.py) serão utilizados.
    - `DB_NAME`: o nome do banco de dados
    - `DB_USER`: o usu rio do banco de dados
    - `DB_PASSWORD`: a senha do usu rio do banco de dados
    - `DB_HOST`: o host do banco de dados
    - `DB_PORT`: a porta do banco de dados
    - `REDIS_URL`: a URL do servidor Redis
4. Execute o comando `python manage.py migrate` para criar as tabelas do banco de dados
5. Execute o comando `python manage.py runserver` para subir a API
    - Caso queira usar o Gunicorn: `gunicorn core.wsgi --bind 0.0.0.0:8000`
6. Abra um navegador e acesse `http://0.0.0.0:8000/batches/` para acessar a API


## Rodando localmente com o uso do Docker (via Docker Compose)

### ⚠️ Para executar este projeto com Docker você precisará instalar em sua máquina o [Docker](https://www.docker.com/) e o [Docker Compose](https://docs.docker.com/compose/install/).

1. Faça o clone do repositório [pig-batch-management-api](https://github.com/marcosalvesdev/pig-batch-management-api) 🐖

2. Para rodar este projeto com o uso do Docker Compose, execute o comando `docker compose up` ou `docker compose up -d` para rodar em background.

3. Após subir o container, execute o comando `docker compose exec web python manage.py migrate` para criar as tabelas do banco de dados.

4. Abra um navegador e acesse `http://0.0.0.0:8000/batches/` para acessar a API.

### ✏️ Caso esteja familiarizado com o uso da ferramenta Make, o arquivo Makefile possui comandos que poderão ser úteis a você.


## Executando testes 🔧

Para executar os testes unitários, execute o comando `python manage.py test` se estiver executando o projeto sem Docker e `docker compose exec web python manage.py test --keepdb --failfast` caso esteja.

## Testes de integraçaõ do sistema 🔧

1. Criando um lote:
    - Faça uma requisição `POST` para `http://0.0.0.0:8000/batches/`
    - Utilize o seguinte JSON como exemplo: `{
        "batch_id": "25",
        "status": "created",
        "piglets_born": 10
    }`
    - Verifique se o mesmo foi criado realizando uma requisição GET para `http://0.0.0.0:8000/batches/`
2. Atualizando um lote:
    - Faça uma requisição `PUT` para `http://0.0.0.0:8000/batches/<id>/`
    - Utilize o seguinte JSON como exemplo: `{
        "status": "created",
        "piglets_born": 5
    }`
    - Verifique se o mesmo foi atualizado realizando uma requisição GET para `http://0.0.0.0:8000/batches/<id>/`
3. Removendo um lote:
    - Faça uma requisição `DELETE` para `http://0.0.0.0:8000/batches/<id>/`
    - Verifique se o lote foi removido realizando uma requisição GET para `http://0.0.0.0:8000/batches/`

Durante cada requisição você pode verificar a quantidade total de leitões realizando uma requisição `GET` para `http://0.0.0.0:8000/batches/get_total_piglets_born/`, a quantidade irá atualizar conforme o sistema for adicionado, removendo ou atualizando a quantidade de leitões em cada lote.



## Principais bibliotecas utilizadas 🔨

- Django==5.1
- djangorestframework==3.15.2
- celery==5.4.0
- redis==5.0.8
- psycopg2-binary==2.9.9
- python-decouple==3.8


## Contatos ✉️

- Email: [marcosalves.dev@gmail.com](mailto:marcosalves.dev@gmail.com)
- LinkedIn: [www.linkedin.com/in/marcos-alves-dev](https://www.linkedin.com/in/marcos-alves-dev)
