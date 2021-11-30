import sqlite3
import os

db_name = "baza.db"

# Refresh DB file
if os.path.exists(db_name):
   os.remove(db_name)
   open(db_name, 'a').close()

# Open connection to DB
con = sqlite3.connect(db_name)
cur = con.cursor()

# Create table users
cur.execute('''CREATE TABLE IF NOT EXISTS users
               (id INTEGER PRIMARY KEY, 
               name TEXT, 
               email TEXT, 
               password TEXT, 
               contact TEXT, 
               created_at TEXT
            )''')

# Fill table users
cur.execute("INSERT INTO users (name, email, password, contact) VALUES (?,?,?,?)",('Ivan',"test@test.com",'123456','00011122233'))

# Create table logins
cur.execute('''CREATE TABLE IF NOT EXISTS logins
               (id INTEGER PRIMARY KEY,
               logins INTEGER,
               last_login TEXT,
               uid INTEGER,
               FOREIGN KEY(uid) REFERENCES user(id)
            )''')

# Create table forgot_password
cur.execute('''CREATE TABLE IF NOT EXISTS forgot_password
               (id INTEGER PRIMARY KEY,
               hash TEXT,
               valid_until TEXT,
               uid INTEGER,
               FOREIGN KEY(uid) REFERENCES user(id)
            )''')

con.commit()

con.close()