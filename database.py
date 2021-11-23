import sqlite3

con = sqlite3.connect('baza.db')
cur = con.cursor()

# Create table
cur.execute('''CREATE TABLE IF NOT EXISTS user
               (id INTEGER PRIMARY KEY, 
               name TEXT, 
               email TEXT, 
               password TEXT, 
               contact TEXT, 
               created_at TEXT)''')

cur.execute("INSERT INTO users (name, email, password, contact) VALUES (?,?,?,?)",('Ivan',"test@test.com",'123456','00011122233'))
con.commit()

con.close()