# Justarter 2024 - Data Pipelines

Esse diretório contém o exemplo prático utilizado no Justarter 2024, com o objetivo de demonstrar a criação de pipelines
de dados com Apache Airflow.

O `postgreSQL` foi utilizado com a base `omdb` disponibilizada no
repositório [credativ/omdb-postgres](https://github.com/credativ/omdb-postgresql) como fonte de dados.

Para acessar o banco de dados, foi feita a instalação do provider `apache-airflow-providers-postgres`:

```shell
pip install apache-airflow-providers-postgres==5.12.0
```

Para usuários do MacOS, é necessário exportar a variável de ambiente `OBJC_DISABLE_INITIALIZE_FORK_SAFETY=yes`

```shell
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=yes
```