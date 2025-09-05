from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator


with DAG(
    dag_id="my_first_dag",
    default_args={
        "owner": "airflow",
        "start_date": "2021-01-01",
        "retries": 1,
    },
    schedule_interval="@daily",
    catchup=False,
) as dag:
    def hello_python_callable():
        print("Hello, Python!")

    hello_python_operator = PythonOperator(
        task_id="hello_python_operator",
        python_callable=hello_python_callable,
    )

    hello_python_operator
