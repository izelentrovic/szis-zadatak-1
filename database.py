import sqlite3

con = sqlite3.connect('baza.db')
cur = con.cursor()

# Create table
cur.execute('''CREATE TABLE IF NOT EXISTS users
               (id INTEGER PRIMARY KEY, 
               name TEXT, 
               email TEXT, 
               password TEXT, 
               contact TEXT, 
               created_at TEXT
            )''')

cur.execute("INSERT INTO users (name, email, password, contact) VALUES (?,?,?,?)",('Ivan',"test@test.com",'123456','00011122233'))

cur.execute('''CREATE TABLE IF NOT EXISTS logins
               (id INTEGER PRIMARY KEY,
               logins INTEGER,
               last_login TEXT,
               uid INTEGER,
               FOREIGN KEY(uid) REFERENCES user(id)
            )''')

con.commit()

con.close()