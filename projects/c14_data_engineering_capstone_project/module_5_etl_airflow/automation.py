 # Import libraries required for connecting to mysql

# Import libraries required for connecting to DB2 or PostgreSql
import mysql.connector
from mysql.connector import Error as MySQLError
import psycopg2
from psycopg2 import Error as PostgreSQLError

# Connect to MySQL

# Connect to DB2 or PostgreSql

# Find out the last rowid from DB2 data warehouse or PostgreSql data warehouse
# The function get_last_rowid must return the last rowid of the table sales_data on the IBM DB2 database or PostgreSql.

def get_last_rowid():
    # Connect to PostgreSQL data warehouse
    conn = psycopg2.connect(
        database="test1",
        user="ahmed",
        password="Admin@123456",
        host="127.0.0.1",
        port="5432"
    )
    cursor = conn.cursor()
    
    # Query the maximum rowid from sales_data
    cursor.execute("SELECT MAX(rowid) FROM sales_data;")
    result = cursor.fetchone()
    
    last_rowid = result[0] if result and result[0] is not None else 0
    
    cursor.close()
    conn.close()
    
    return last_rowid


last_row_id = get_last_rowid()
print("Last row id on production datawarehouse = ", last_row_id)

# List out all records in MySQL database with rowid greater than the one on the Data warehouse
# The function get_latest_records must return a list of all records that have a rowid greater than the last_row_id in the sales_data table in the sales database on the MySQL staging data warehouse.

def get_latest_records(rowid):
    # Connect to MySQL staging database
    connection = mysql.connector.connect(
        host='localhost',
        database='sales',
        user='ahmed_pwd',
        password='Admin@123456'
    )
    cursor = connection.cursor()
    
    # Query all records with rowid greater than last_rowid
    query = "SELECT rowid, product_id, customer_id, price, quantity, sale_timestamp FROM sales_data WHERE rowid > %s;"
    cursor.execute(query, (rowid,))
    records = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return records

new_records = get_latest_records(last_row_id)

print("New rows on staging datawarehouse = ", len(new_records))

# Insert the additional records from MySQL into DB2 or PostgreSql data warehouse.
# The function insert_records must insert all the records passed to it into the sales_data table in IBM DB2 database or PostgreSql.

def insert_records(records):
    if not records:
        print("No new records to insert.")
        return
        
    # Connect to PostgreSQL data warehouse
    conn = psycopg2.connect(
        database="test1",
        user="ahmed",
        password="Admin@123456",
        host="127.0.0.1",
        port="5432"
    )
    cursor = conn.cursor()
    
    # Insert records into PostgreSQL sales_data
    insert_sql = """
    INSERT INTO sales_data (rowid, product_id, customer_id, price, quantity, timeestamp)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (rowid) DO NOTHING;
    """
    
    cursor.executemany(insert_sql, records)
    conn.commit()
    
    cursor.close()
    conn.close()

insert_records(new_records)
print("New rows inserted into production datawarehouse = ", len(new_records))

# disconnect from mysql warehouse

# disconnect from DB2 or PostgreSql data warehouse 

# End of program
