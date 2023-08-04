import sqlite3  
import os

def databasecreation():
    if "database.sqlite3" not in os.listdir():
        con = sqlite3.connect("database.sqlite3") 
        print("Database opened successfully")     
        con.execute("CREATE TABLE registration (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT NOT NULL, phone TEXT NOT NULL, password TEXT NOT NULL)")  
        print("Table created successfully")  
        con.close() 
        return 'database created' 
    else:
        return 'already have database'
    
 