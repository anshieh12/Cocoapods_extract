
import os
import json
from fnmatch import fnmatch
import psycopg2
from filecmp import dircmp




#variable declaration
root = input ("Please input the new path where you want to scan/compare the repo and populate to database: ")
root_bk = input ("Please input the backup path where you want to scan/compare the repo: ")
dbname = input ("Please input the database name: ")
user =  input ("Please input the database username: ")
password =  input ("Please input the database password: ")

pattern = "*podspec.json"
select_query_library = 'select id from library where name = %s'
insert_query_library ='''insert into library (name, description) values (%s, %s) returning id;'''
insert_query_library_version ='''insert into library_version (version, license,library_id) values (%s, %s,%s) returning id;'''

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
    

def select_record_fetchone(conn,cursor, query,value):
    cursor.execute(query,(value,))
    conn.commit()
    return cursor.fetchone()


def insert_record(conn,cursor, query,value):
    cursor.execute(query,value)
    conn.commit()
    return cursor.fetchone() 


# function that opens json files and parses information to populate postgres tables
def populate_db(conn,cursor, filename):
    with open(filename) as f:
        data = json.load(f)
        print(data)

        uniq_name = data.get('name', "")
        fk_id = -1

        # get id from library table with the current name
        temp_id = select_record_fetchone(conn,cursor, select_query_library,uniq_name)
        print(temp_id)
        
        # if id exist in the table already, assign library_id from library_version table to it
        if (temp_id != None):
            fk_id = int(temp_id[0])
        # if not, insert name, description and auto-incremented id into library table and then assign the id to library_id
        else:
            record_insert_library = (uniq_name,data.get('description', ""))
            fk_id = insert_record(conn,cursor, insert_query_library, record_insert_library)
            
        # insert auto-incremented id, version, license and library_id into library_version table
        record_insert_library_version = (data.get('version', ""), json.dumps(data.get('license', "")),fk_id)
        print ('record_insert_library_version ',record_insert_library_version)
        insert_record(conn,cursor, insert_query_library_version, record_insert_library_version)
 


# function that compares the old and new repo
def check_new_files(dcmp):
    # find files that are only in the new repo
    for name in dcmp.left_only:
        new_info[name] = [dcmp.left]
        print("A new file: %s found in %s" % (name, dcmp.left)) 
    
    # go into subdirectories
    for sub_dcmp in dcmp.subdirs.values():
        check_new_files(sub_dcmp)


# check for updates and populate table
new_info = {}

# create a directory comparison object (dcmp)
dcmp = dircmp(root,root_bk) 
# looking for newly added files and store file information in new_info
check_new_files(dcmp) 

conn = establish_connection()
cursor = get_cursor(conn)
print ("cursor", cursor)
for file_name, folder_path in new_info.items():
    for path, subdirs, files in os.walk(folder_path[0]+'/'+file_name):
        print(folder_path[0]+'/'+file_name)
        for name in files:
            #print (path)
            if fnmatch(name, pattern):
                path = os.path.join(path, name)
                print (path,name)
                populate_db(conn,cursor, path)

close_connection(conn,cursor)






