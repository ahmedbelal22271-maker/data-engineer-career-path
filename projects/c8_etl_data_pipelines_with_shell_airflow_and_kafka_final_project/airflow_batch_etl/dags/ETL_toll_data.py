from datetime import timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

# ==============================================================================
# CONFIGURATION & CONSTANTS
# ==============================================================================
DEST_DIR = '/home/project/airflow/dags/finalassignment/destination'

# Task 1.1: Define DAG arguments
default_args = {
    'owner': 'dummy_owner',
    'start_date': days_ago(1),
    'email': ['dummy@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Task 1.2: Define the DAG
dag = DAG(
    'ETL_toll_data',
    default_args=default_args,
    description='Apache Airflow Final Assignment',
    schedule_interval=timedelta(days=1),
)

# ==============================================================================
# TASK DEFINITIONS (Exercise 2)
# ==============================================================================

# Task 2.1: Unzip data
unzip_data = BashOperator(
    task_id='unzip_data',
    bash_command=f'tar -xzf "{DEST_DIR}/tolldata.tgz" -C "{DEST_DIR}"',
    dag=dag,
)

# Task 2.2: Extract data from CSV file
extract_data_from_csv = BashOperator(
    task_id='extract_data_from_csv',
    bash_command=f'cut -d"," -f1-4 "{DEST_DIR}/vehicle-data.csv" > "{DEST_DIR}/csv_data.csv"',
    dag=dag,
)

# Task 2.3: Extract data from TSV file
extract_data_from_tsv = BashOperator(
    task_id='extract_data_from_tsv',
    bash_command=f'cut -f5-7 "{DEST_DIR}/tollplaza-data.tsv" | tr "\t" "," > "{DEST_DIR}/tsv_data.csv"',
    dag=dag,
)

# Task 2.4: Extract data from fixed-width file
extract_data_from_fixed_width = BashOperator(
    task_id='extract_data_from_fixed_width',
    bash_command=f'cut -c 59-67 "{DEST_DIR}/payment-data.txt" | tr " " "," > "{DEST_DIR}/fixed_width_data.csv"',
    dag=dag,
)

# Task 2.5: Consolidate extracted data
consolidate_data = BashOperator(
    task_id='consolidate_data',
    bash_command=f'paste -d"," "{DEST_DIR}/csv_data.csv" "{DEST_DIR}/tsv_data.csv" "{DEST_DIR}/fixed_width_data.csv" > "{DEST_DIR}/extracted_data.csv"',
    dag=dag,
)

# Task 2.6: Transform data (uppercase vehicle_type)
transform_data = BashOperator(
    task_id='transform_data',
    bash_command=f'tr "[:lower:]" "[:upper:]" < "{DEST_DIR}/extracted_data.csv" > "{DEST_DIR}/transformed_data.csv"',
    dag=dag,
)

# ==============================================================================
# TASK PIPELINE DEPENDENCIES (Task 2.7)
# ==============================================================================
unzip_data >> extract_data_from_csv >> extract_data_from_tsv >> extract_data_from_fixed_width >> consolidate_data >> transform_data
