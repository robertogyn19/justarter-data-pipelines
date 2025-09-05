# Justarter 2024 - Data Pipelines

Esse diretório contém o exemplo prático utilizado no Justarter 2024, com o objetivo de demonstrar a criação de pipelines
de dados com Apache Airflow.

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

Para acessar o banco de dados, foi feita a instalação do provider `apache-airflow-providers-postgres`:

```shell
pip install apache-airflow-providers-postgres==5.12.0
```

Para usuários de MacOS, é necessário exportar a variável de ambiente `OBJC_DISABLE_INITIALIZE_FORK_SAFETY=yes`

```shell
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=yes
```