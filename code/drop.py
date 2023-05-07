import psycopg2
import psycopg2.extras as extras

def pgsql_connect(user, password, host, port, database):
    
    conn = psycopg2.connect(user = user,
                            password = password,
                            host = host,
                            port = port,
                            database = database)
    return conn

def drop_table_2(conn):

    cursor = conn.cursor()
  
    sql = '''DROP TABLE wind_project.wind;'''
  
    cursor.execute(sql)
  
    conn.commit()

def drop_table_1(conn):

    cursor = conn.cursor()
  
    sql = '''DROP TABLE wind_project.temperature; '''
  
    cursor.execute(sql)
  
    conn.commit()

def drop_schema(conn):

    cursor = conn.cursor()
  
    sql = '''DROP SCHEMA "wind_project";'''
  
    cursor.execute(sql)
  
    conn.commit()

if __name__ == '__main__':

    conn = pgsql_connect("postgres", "pass", "localhost", "5431", "postgres")
    drop_table_1(conn)
    drop_table_2(conn)
    drop_schema(conn)
    conn.close()

