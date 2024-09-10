import humanize
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import SQLExecuteQueryOperator

CONN_ID = "postgres_default"
DATABASE = "omdb"
TABLE_NAME = "public.top_profitable_movies"

with (DAG(
  dag_id="etl_dag",
  default_args={
    "owner": "airflow",
    "start_date": "2021-01-01",
    "retries": 1,
  },
  schedule_interval="@daily",
  catchup=False,
) as dag):
  get_sql = """
    SELECT id, name, revenue, budget, revenue - budget as profit
    FROM public.movies
    WHERE revenue > budget
    ORDER BY profit DESC
    LIMIT 10
  """

  # task 01
  top_profitable_movies = SQLExecuteQueryOperator(
    task_id="top_profitable_movies",
    conn_id=CONN_ID,
    database=DATABASE,
    show_return_value_in_logs=True,
    sql=get_sql,
    hook_params={"options": "-c statement_timeout=3000ms"},
  )


  def transform_fn(top_profitable_movies):
    for movie in top_profitable_movies:
      movie.append(humanize.intword(movie[4]))

    return top_profitable_movies


  # task 02
  transform = PythonOperator(
    task_id="transform",
    python_callable=transform_fn,
    op_args=[top_profitable_movies.output],
  )

  # task 03
  drop_table = SQLExecuteQueryOperator(
    task_id="drop_table",
    conn_id=CONN_ID,
    database=DATABASE,
    sql=f"DROP TABLE {TABLE_NAME}",
    retries=0,
  )

  sql_create_table = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
      id         INT PRIMARY KEY,
      name       TEXT,
      revenue    BIGINT,
      budget     BIGINT,
      profit     BIGINT,
      profit_fmt TEXT
    )
  """

  # task 04
  # Essa tarefa só será executada se todas as tarefas anteriores forem finalizadas, independentemente do status
  create_table = SQLExecuteQueryOperator(
    task_id="create_table",
    conn_id=CONN_ID,
    database=DATABASE,
    sql=sql_create_table,
    trigger_rule="all_done",
  )

  insert_sql = f"""
      INSERT INTO {TABLE_NAME} (id, name, revenue, budget, profit, profit_fmt) VALUES
    """


  def prepare_insert_query_fn(movies: list):
    value = ", ".join(
      f"({movie[0]}, '{movie[1]}', {movie[2]}, {movie[3]}, {movie[4]}, '{movie[5]}')" for movie in movies
    )
    return f"{insert_sql} {value}"


  # task 05
  prepare_insert_query = PythonOperator(
    task_id="prepare_insert_query",
    python_callable=prepare_insert_query_fn,
    op_args=[transform.output],
  )

  # task 06
  insert_movies = SQLExecuteQueryOperator(
    task_id="insert_movies",
    conn_id=CONN_ID,
    database=DATABASE,
    sql="""{{ ti.xcom_pull(task_ids='prepare_insert_query') }}""",
    trigger_rule="all_done",
  )

  top_profitable_movies >> transform >> drop_table >> create_table >> prepare_insert_query >> insert_movies
