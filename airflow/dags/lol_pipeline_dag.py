from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import sys

sys.path.insert(0, '/opt/airflow')

default_args = {
    'owner': 'vlado',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='lol_pipeline',
    description='End-to-end League of Legends RAM data pipeline',
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule_interval='0 9 * * *',  #Runs daily at 9 AM
    catchup=False,
    tags=['lol', 'aram', 'pipeline'],
) as dag:

    #Task 1: Extract matches from Riot Games API
    def run_extraction():
        from extraction.riot_extractor import extract_matches_for_player
        extract_matches_for_player("Doblado", "WeebR", match_count=20)

    extract_task = PythonOperator(
        task_id='extract_matches',
        python_callable=run_extraction,
    )

    #Task 2: Load raw JSON files into PostgreSQL
    def run_loading():
        from loading.load_to_postgres import load_all_matches
        load_all_matches()

    load_task = PythonOperator(
        task_id='load_to_postgres',
        python_callable=run_loading,
    )

    #Task 3: Run dbt transformations
    dbt_task = BashOperator(
        task_id='run_dbt',
        bash_command='cd /opt/airflow/dbt/lol_dbt && dbt run --profiles-dir /opt/airflow/dbt/lol_dbt',
    )

    #Execution order
    extract_task >> load_task >> dbt_task