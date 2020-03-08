
import os
import json
import psycopg2


create_table_library = '''CREATE TABLE library(
          id SERIAL PRIMARY KEY,
          name VARCHAR(250),
          description TEXT
);'''
# create the library_version table
create_table_library_ver = '''CREATE TABLE library_version(
            id SERIAL PRIMARY KEY,
            version VARCHAR(100),
            license TEXT,
            library_id INTEGER NOT NULL, FOREIGN KEY(library_id) REFERENCES library(id)
);'''


dbname = input ("Please input the database name: ")
user =  input ("Please input the database username: ")
password =  input ("Please input the database password: ")

def establish_connection(): 
    #Establishing the connection with postgres
    conn = psycopg2.connect(
       dbname= dbname,user=user, password=password, host='127.0.0.1', port= '5432'
    )
    print ("connection ",conn)
    return conn



def get_cursor(conn):
    return conn.cursor()



def close_connection(conn,cursor):
    conn.commit()
    cursor = None
    conn.close()
    




def create_table(conn,cursor, query):
    #print ("cursor", cursor)
    #print ("query", query)
    cursor.execute(query)
    print ("Table created")
    conn.commit()





# create table
conn = establish_connection()
cursor = get_cursor(conn)
print ("cursor", cursor)
create_table(conn,cursor,create_table_library)
create_table(conn,cursor,create_table_library_ver)
close_connection(conn,cursor)
