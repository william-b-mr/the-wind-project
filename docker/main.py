import pandas as pd
import psycopg2
import psycopg2.extras as extras
import numpy as np
import requests

params_api = {"lat":"-3.803",
           "long":"-38.410",
           "start_date":"2023-02-15",
           "end_date":"2023-05-06",
           "params":"temperature_2m,windspeed_10m,windspeed_100m,winddirection_10m,winddirection_100m,windgusts_10m"}

def pgsql_connect(user, password, host, port, database):
    
    conn = psycopg2.connect(user = user,
                            password = password,
                            host = host,
                            port = port,
                            database = database)
    return conn


def create_schema(conn):

    cursor = conn.cursor()
  
    sql = '''CREATE SCHEMA "wind_project"; '''
  
    cursor.execute(sql)
  
    conn.commit()

def create_table_1(conn):

    cursor = conn.cursor()
  
    sql = '''CREATE TABLE wind_project.wind(timestamp TIMESTAMP, speed_10 FLOAT, speed_100 FLOAT, gusts_10 FLOAT, direction_10 FLOAT, direction_100 FLOAT);'''
  
    cursor.execute(sql)
  
    conn.commit()

def create_table_2(conn):

    cursor = conn.cursor()
  
    sql = '''CREATE TABLE wind_project.temperature(timestamp TIMESTAMP, temperature_2 FLOAT);'''
  
    cursor.execute(sql)
  
    conn.commit()

def execute_values(conn, df, table):
  
    tuples = [tuple(x) for x in df.to_numpy()]
  
    cols = ','.join(list(df.columns))
    # SQL query to execute
    query = "INSERT INTO %s(%s) VALUES %%s" % (table, cols)
    cursor = conn.cursor()
    try:
        extras.execute_values(cursor, query, tuples)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 1
    print("the dataframe is inserted")
    cursor.close()

def get_hourly_data_2(params):
    
    lat = params["lat"]
    long = params["long"]
    start_dt = params["start_date"]
    end_dt = params["end_date"]
    params = params["params"]
    
    get_body = f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={long}&start_date={start_dt}&end_date={end_dt}&hourly={params}"
    
    resp_full = requests.get(get_body)
    
    body = resp_full.json()

    df = pd.DataFrame(body['hourly'])
    
    return df

def preprocess(df):
    df.rename(columns = {'time':'timestamp',
                       'temperature_2m':'temperature_2',
                       'windspeed_10m':'speed_10',
                       'windspeed_100m':'speed_100',
                       'winddirection_10m':'direction_10',
                       'winddirection_100m':'direction_100',
                       'windgusts_10m':'gusts_10'}, inplace = True)
    return df

if __name__ == '__main__':

    conn = pgsql_connect("postgres", "pass", "localhost", "5431", "postgres")
    create_schema(conn)
    create_table_1(conn)
    create_table_2(conn)
    df = get_hourly_data_2(params_api)
    df_pp = preprocess(df)
    execute_values(conn, df_pp[['timestamp','temperature_2']], 'wind_project.temperature')
    execute_values(conn, df_pp.drop(columns = 'temperature_2'), 'wind_project.wind')

    conn.close()


