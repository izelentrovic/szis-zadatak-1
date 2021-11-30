import hashlib
import sqlite3
from datetime import date, datetime, timedelta
import time

con = sqlite3.connect('baza.db')


def login():
        ime = input("Unesi ime: ")
        lozinka = input("Unesi lozinku: ")
        
        cur = con.cursor()
        row=cur.execute("SELECT id, password FROM users WHERE name = ?", (ime,))
        row=cur.fetchone()
        uid = row[0]
        password = row[1]

        if(cur.rowcount<=0):
            print(uid, password)
            return
        
        print("Korisnik postoji i prijavljen \n")
        now = date.today()

        logins = 0

        cur.execute('''UPDATE logins 
                    SET logins = ?,
                    last_login = ?
                    WHERE uid = ?
                    ''', (logins+1, now, uid))

        cur.execute('''INSERT INTO logins
                    (logins, last_login, uid)
                    VALUES (?, ?, ?)
                    ''', (logins+1, now, uid))

        cur.execute(f'''INSERT OR REPLACE INTO logins 
                    (logins, last_login, uid) 
                    VALUES (
                        (SELECT logins FROM logins WHERE Name = "SearchName"),
                        {now},
                        IFNULL(
                            (SELECT COUNT FROM logins WHERE Name = "SearchName")
                            , 0) 
                        + 1)
        ''')
        cur.commit()

        
def registracija():
        ime = input("Unesi ime: ")
        email = input("Unesi email: ")
        lozinka = input("Unesi lozinku: ")
        kontakt = input("Unesi kontakt broj: ")
        today = date.today() #danasnji datum

        hash_object = hashlib.md5(lozinka.encode())
        safelozinka = hash_object.hexdigest()

        cur = con.cursor()
        
        cur.execute("INSERT INTO users (name, email, password, kontakt, created_at) VALUES (?,?,?,?,?)",(ime, email, safelozinka, kontakt, today))
        con.commit()


        if(cur.rowcount>0):
                print("Podatak je zapisan")
                
        con.close()
        
def forgot_password():
    cur = con.cursor()
    
    email = input("Unesi email: ")
    
    cur.execute("SELECT id FROM users WHERE email=?", (email,))
    
    row = cur.fetchone()
    
    if(row == None):
        print("Korisnik nije pronađen!")
        return

    uid = row[0]
    
    curr_time = int(time.time())
    plus_30_time = datetime.now() + timedelta(minutes=30)

    hash_object = hashlib.md5(str(curr_time).encode())
    hashed_time = hash_object.hexdigest()
    
    cur.execute("INSERT INTO forgot_password (hash, valid_until, uid) VALUES (?,?,?)", (hashed_time, plus_30_time, uid))
    con.commit()

    if(cur.rowcount>0):
        print("Hash:", hashed_time)
    
    con.close()

def main():
    print("Dobrodošli u Unidu sustav!")
    print("Za prijavu upišite broj 1, za registraciju broj 2, za zaboravljenu lozinku broj 3:")

    unos = 0

    while(unos!=1 and unos!=2 and unos!=3):
        unos = int(input("Unesite broj: "))

    if(unos==3):
        forgot_password()

    if(unos==2):
        registracija()
        
    if(unos==1):
        login()


if __name__=="__main__":
    main()