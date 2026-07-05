from datetime import datetime
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import sqlite3



def log_progress(logged_text):
    timestamp_format = '%Y-%h-%d-%H:%M:%S' 
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)

    with open("code_log.txt",'a') as f:
        f.write(timestamp + " : " + logged_text + '\n')


def extract(url):
    html_page = requests.get(url).text
    soup = BeautifulSoup(html_page,'html.parser')

    tables = soup.find_all('table')
    
    table = tables[0]
    rows = table.find_all('tr')
    
    

    df = pd.DataFrame(data = [],columns = ['Name', 'MC_USD_Billion'])
    for row in rows[1:]:
        cols = row.find_all('td')
        bank_name = cols[1].get_text(strip=True)
        market_cap = cols[2].get_text(strip=True).replace('\n','')
        market = float(market_cap)
        df_to_append = pd.DataFrame(data = [[bank_name,market]],
                                    columns = ['Name', 'MC_USD_Billion'])
        df = pd.concat([df,df_to_append],ignore_index=True)

    return df

def transform(df):
    df_exchange = pd.read_csv(csv_path)
    exchange_rate_dict = df_exchange.set_index('Currency').to_dict()['Rate']
    
    gbp_rate = float(exchange_rate_dict['GBP'])
    df['MC_GBP_Billion'] = [np.round(x*gbp_rate, 2) for x in df['MC_USD_Billion']]
    
    eur_rate = float(exchange_rate_dict['EUR'])
    df['MC_EUR_Billion'] = [np.round(x*eur_rate, 2) for x in df['MC_USD_Billion']]
    
    inr_rate = float(exchange_rate_dict['INR'])
    df['MC_INR_Billion'] = [np.round(x*inr_rate, 2) for x in df['MC_USD_Billion']]
    

def load_to_csv(df, output_path):
    df.to_csv(output_path, index=False)


def load_to_db(df, sql_connection, table_name):
    df.to_sql(table_name, sql_connection, if_exists='replace', index=False)

def run_query(query_statement, sql_connection):
    print(query_statement)
    query_output = pd.read_sql_query(query_statement, sql_connection)
    print(query_output)

url = "https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks"
csv_path = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMSkillsNetwork-PY0221EN-Coursera/labs/v2/exchange_rate.csv"
output_csv_path = "./Largest_banks_data.csv"
database_name = "Banks.db"
table_name = "Largest_banks"
log_file = "code_log.txt"
conn = sqlite3.connect('Banks.db')

log_progress("SQL Connection initiated")
    
log_progress("Preliminaries complete. Initiating ETL process")

df = extract(url)
print(df)

log_progress("Data extraction complete. Initiating Transformation process")

transform(df)
print(df)

log_progress("Data transformation complete. Initiating Loading process")

load_to_csv(df, output_csv_path)

log_progress("Data saved to CSV file")

load_to_db(df, conn, table_name)

log_progress("Data loaded to Database as a table, Executing queries")

log_progress("Process Complete")

run_query("SELECT * FROM Largest_banks", conn)
run_query("SELECT AVG(MC_GBP_Billion) FROM Largest_banks", conn)
run_query("SELECT Name FROM Largest_banks LIMIT 5", conn)

conn.close()
log_progress("Server Connection closed")

