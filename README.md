# Pipeline de dados com Airflow

## Instalação

Existe várias formas para instalar o Airflow, por exemplo:
1. Utilizar o comando `pip install apache-airflow` para instalar o Airflow e suas dependências.
2. Utilizar um docker-compose.
3. Utilizar o Astro CLI.

### 1. Instalação com pip

Essa forma é a mais direta, porém, é necessário ter um ambiente python local.
Abaixo temos os comandos necessários para realizar a instalação, para mais detalhes, veja a [documentação oficial](https://airflow.apache.org/docs/apache-airflow/stable/installation/installing-from-pypi.html).

```shell
# Ambiente - a utilização de um ambiente virtual é recomendada
python -m venv .venv

# Instalação
pip install "apache-airflow[celery]==2.10.1" \
  --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.10.1/constraints-3.12.txt"
```

### 2. Instalação com docker-compose

Para ambientes com o docker disponível, uma opção mais simples é utilizar o docker-compose.
Veja a [documentação oficial](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html) para mais detalhes.

```shell
# obtenção do docker-compose
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.10.1/docker-compose.yaml'

# instalação  
docker-compose up

# inicialização
???
```

### 3. Instalação com Astro CLI

O Astro CLI é uma ferramenta que facilita a instalação e configuração do Airflow.
Para instalar o [Astro CLI](https://www.astronomer.io/docs/astro/cli/overview), execute o comando abaixo:

```shell
# No macOS
brew install astro-cli

# No linux
curl -sSL install.astronomer.io | sudo bash -s
```