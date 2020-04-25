import psycopg2
import csv

DBNAME = 'postgres'
USER = 'postgres'
HOST = 'localhost'
PASSWORD = '1234'
PORT = '5432'

"""
CREATE EXTENSION cube;
CREATE EXTENSION earthdistance;
"""

# Creating Connection With Database
try:
    connection = psycopg2.connect("dbname='{}' user='{}' host='{}' password='{}' port='{}'".format(DBNAME,USER,HOST,PASSWORD,PORT))
    print("Connection to the Database Succeeded!")
except:
    print("Connection Error")
    exit(0)
    
# Creating Table in Database    
try:
    cursor = connection.cursor()
    create_table_query = '''CREATE TABLE pincode (
                    key TEXT PRIMARY KEY,
                    place TEXT,
                    admin TEXT,
                    lat REAL,
                    long REAL,
                    acc INT);'''
    cursor.execute(create_table_query)
    cursor.close()
    connection.commit()
    print("Table created successfully in PostgreSQL ")
except (Exception, psycopg2.DatabaseError) as error:
    print("Table could not be created!")
    print(error)
    exit(0)
    
# Inserting All Records From CSV File into Database
try:
    cursor = connection.cursor()
    file = open('IN.csv')
    data = csv.reader(file)
    next(data) # Skips Header Row
    for rec in data:
        rec = ['NULL' if (element == '') else element for element in rec]
        insert_table_query = "INSERT INTO pincode(key, place, admin, lat, long, acc) VALUES('%s','%s','%s',%s,%s,%s);"%(rec[0],rec[1], rec[2], rec[3], rec[4], rec[5])
        cursor.execute(insert_table_query)
    cursor.close()
    connection.commit()
    connection.close()    
    file.close()
    print("All Records Inserted!")
except:
    print("Record Insertion Error")
    exit(0)