# JusStarter - Pipeline de dados com Airflow

## 1. Instalação

Existe várias formas para instalar o Airflow, por exemplo:

1. Utilizar o comando `pip install apache-airflow` para instalar o Airflow e suas dependências.
2. Utilizar um docker-compose.
3. Utilizar o Astro CLI.

### 1.1. Instalação com pip

Essa forma é a mais direta, porém, é necessário ter um ambiente python local.
Abaixo temos os comandos necessários para realizar a instalação, para mais detalhes, veja
a [documentação oficial](https://airflow.apache.org/docs/apache-airflow/stable/installation/installing-from-pypi.html).

```shell
# Ambiente - a utilização de um ambiente virtual é recomendada
python -m venv .venv

# Instalação
pip install "apache-airflow[celery]==2.11.0" \
  --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.11.0/constraints-3.12.txt"
```

Após a instalação, ainda é necessário realizar o bootstrap do Airflow.
O comando `airflow standalone` inicializará o banco de dados, criará um usuário e criará a estrutura de diretórios e
arquivos necessários. Observe no comando abaixo que configuramos a variável de ambiente `AIRFLOW_HOME` para o diretório
`airflow-with-pip`.

```shell
export AIRFLOW_HOME=$(pwd)/airflow-with-pip
cd airflow-with-pip
airflow standalone
```

### 1.2. Instalação com docker-compose

Para ambientes com o docker disponível, uma opção mais simples é utilizar o docker-compose.
Veja a [documentação oficial](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)
para mais detalhes.

O docker-compose.yaml foi obtido da documentação oficial, e o diretório `airflow-with-docker-compose` foi criado para
conter os arquivos necessários.

```shell
cd airflow-with-docker-compose

# pull das imagens
docker compose pull

# build
docker compose build

# configuração do owner dos diretórios
mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env

# inicialização (usuário: airflow, senha: airflow)
docker compose up airflow-init

# inicialização do Airflow
docker compose up
```

Após a execução dos comandos acima, acesse o Airflow em `http://localhost:8080`.
Os dados de acesso são: usuário `airflow` e senha `airflow`.

### 1.3. Instalação com Astro CLI

O Astro CLI é uma ferramenta que facilita a instalação e configuração do Airflow.
Para instalar o [Astro CLI](https://www.astronomer.io/docs/astro/cli/overview), execute o comando abaixo:
O diretório `airflow-with-astro` foi criado com o Astro CLI, com o comando `astro dev init`, com todas as configurações
necessárias e um exemplo de DAG.

```shell
# No macOS
brew install astro

# No linux
curl -sSL install.astronomer.io | sudo bash -s

# Inicialização
cd airflow-with-astro
astro dev init --airflow-version 2.11.0 --from-template=learning-airflow

# Inicialização do Airflow
astro dev start
```

## 2. Banco de dados

O `postgreSQL` foi utilizado com a base `omdb` disponibilizada no
repositório [credativ/omdb-postgres](https://github.com/credativ/omdb-postgresql) como fonte de dados.
Abaixo tem a sequência de comandos para inicializar o banco de dados, fazer o download do backup e restaurar o mesmo:

```shell
# Inicialização do banco de dados
$ docker run --name postgres --publish 5432:5432 -e POSTGRES_PASSWORD=postgres -dit postgres:16
525dbadac19d0eec24e82f1320744725fa2539b6c910f7f04b53ef0eb1d990f1

# download do backup da base de dados
$ wget https://github.com/credativ/omdb-postgresql/releases/download/2023-09-27/omdb.dump

# Criação do banco que irá receber os dados
$ docker exec -i postgres psql -U postgres -d postgres -c "CREATE DATABASE omdb;"
CREATE DATABASE

# Restauração do backup (observe que na saída é esperado um o erro do schema public já existente)
$ docker exec -i postgres pg_restore -U postgres -d omdb < omdb.dump
pg_restore: error: could not execute query: ERROR:  schema "public" already exists
Command was: CREATE SCHEMA public;

pg_restore: warning: errors ignored on restore: 1
```

Abaixo tem um comando SQL para validar a restauração, retornando os 5 filmes com maior receita:

```shell
# Validação
$ docker exec -it postgres psql -U postgres -d omdb -c "SELECT id,name,budget,revenue FROM movies WHERE revenue is not null ORDER BY revenue DESC LIMIT 5"
   id   |           name           |  budget   |  revenue   
--------+--------------------------+-----------+------------
 120104 | Avengers: Endgame        | 356000000 | 2797501328
  26301 | Avatar                   | 237000000 | 2787965087
    597 | Titanic                  | 200000000 | 2187463944
  31510 | Avatar: The Way of Water | 285000000 | 2176229105
  69531 | Star Wars: Episode VII   | 245000000 | 2068223624
(5 rows)
```

## 3. Dependências adicionais

Para integrar o Airflow com o PostgreSQL, precisamos instalar o provider `apache-airflow-providers-postgres`.
A forma de instalação vai depender da forma que o Airflow foi instalado, se foi com `pip`, `docker-compose` ou
`Astro CLI`.

### 3.1. Instalação com pip

```shell
pip install apache-airflow-providers-postgres==5.12.0
```

### 3.2. Instalação com docker-compose

Se você estiver executando com o docker-compose, o provider já está instalado, esse procedimento está
documentado [aqui](https://airflow.apache.org/docs/apache-airflow/2.11.0/howto/docker-compose/index.html#special-case-adding-dependencies-via-requirements-txt-file).
Isso foi feito adicionado o arquivo `requirements.txt` com o conteúdo abaixo:

```
apache-airflow-providers-postgres
```

E também adicionado um `Dockerfile` customizado com o conteúdo abaixo:

```Dockerfile
FROM apache/airflow:2.11.0
COPY requirements.txt .
RUN pip install apache-airflow==${AIRFLOW_VERSION} -r requirements.txt
```

E o `docker-compose.yaml` foi alterado para fazer o build da imagem customizada.

### 3.3. Instalação com Astro CLI

Se você estiver executando com o Astro CLI, o provider já está instalado.

## 4. Configuração do Airflow

Para conectar o Airflow com o PostgreSQL, precisamos criar uma conexão no Airflow.
Acesse o Airflow em `http://localhost:8080`, clique em `Admin` -> `Connections` e depois clique no botão `+` para
adicionar uma nova conexão.
Preencha os campos conforme abaixo:

- Conn Id: `omdb_postgres`
- Conn Type: `Postgres`
- Host: `host.docker.internal` (se estiver utilizando o docker-compose ou Astro CLI no Windows ou macOS, caso contrário
  utilize `localhost`)
- Database: `omdb`
- Port: `5432`
- Login: `postgres`
- Password: `postgres`
- Extra: `{"ssl_mode": "disable"}`

Clique em `Save` para salvar a conexão.

## 5. DAGs

As DAGs estão no diretório `dags`, com dois exemplos:

- `my_first_dag.py`: um exemplo simples de DAG que imprime a mensagem `Hello, Python!`.
- `etl_dag.py`: um exemplo de DAG que extrai dados do banco de dados PostgreSQL, transforma os dados e insere de
  volta no banco.

Para que as DAGs sejam carregadas, copie o diretório `dags` para o diretório de DAGs do Airflow.
Se você está rodando o Airflow com `pip`, o diretório de DAGs é `$(pwd)/airflow-with-pip/dags`.
Se você está rodando o Airflow com `docker-compose`, o diretório de DAGs é `$(pwd)/airflow-with-docker-compose/dags`.
Se você está rodando o Airflow com `Astro CLI`, o diretório de DAGs é `$(pwd)/airflow-with-astro/dags`.