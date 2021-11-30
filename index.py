import hashlib
import sqlite3
from datetime import date, datetime, timedelta
import time

class Account():
    def __init__(self):
        self.con = sqlite3.connect('baza.db')
        self.cur = self.con.cursor()

    def __del__(self):
        self.con.close()

    def login(self):
            ime = input("Unesi ime: ")
            lozinka = input("Unesi lozinku: ")

            row=self.cur.execute("SELECT id, password FROM users WHERE name = ?", (ime,))
            row=self.cur.fetchone()
            uid = row[0]
            password = row[1]

            if(self.cur.rowcount<=0):
                print(uid, password)
                return
            
            print("Korisnik postoji i prijavljen \n")
            now = date.today()

            logins = 0

            self.cur.execute('''UPDATE logins 
                        SET logins = ?,
                        last_login = ?
                        WHERE uid = ?
                        ''', (logins+1, now, uid))

            self.cur.execute('''INSERT INTO logins
                        (logins, last_login, uid)
                        VALUES (?, ?, ?)
                        ''', (logins+1, now, uid))

            self.cur.execute(f'''INSERT OR REPLACE INTO logins 
                        (logins, last_login, uid) 
                        VALUES (
                            (SELECT logins FROM logins WHERE Name = "SearchName"),
                            {now},
                            IFNULL(
                                (SELECT COUNT FROM logins WHERE Name = "SearchName")
                                , 0) 
                            + 1)
            ''')
            self.cur.commit()
            
    def registracija(self):
            ime = input("Unesi ime: ")
            email = input("Unesi email: ")
            lozinka = input("Unesi lozinku: ")
            kontakt = input("Unesi kontakt broj: ")
            today = date.today() #danasnji datum

            hash_object = hashlib.md5(lozinka.encode())
            safelozinka = hash_object.hexdigest()
            
            self.cur.execute("INSERT INTO users (name, email, password, kontakt, created_at) VALUES (?,?,?,?,?)",(ime, email, safelozinka, kontakt, today))
            self.con.commit()

            if(self.cur.rowcount>0):
                    print("Podatak je zapisan")
            
    def forgot_password(self):
        
        email = input("Unesi email: ")
        
        self.cur.execute("SELECT id FROM users WHERE email=?", (email,))
        
        row = self.cur.fetchone()
        
        if(row == None):
            print("Korisnik nije pronađen!")
            return

        uid = row[0]
        
        self.curr_time = int(time.time())
        plus_30_time = datetime.now() + timedelta(minutes=30)

        hash_object = hashlib.md5(str(self.curr_time).encode())
        hashed_time = hash_object.hexdigest()
        
        self.cur.execute("INSERT INTO forgot_password (hash, valid_until, uid) VALUES (?,?,?)", (hashed_time, plus_30_time, uid))
        self.con.commit()

        if(self.cur.rowcount>0):
            print("Hash:", hashed_time)

    def reset_password(self, hash):
        email = input("Unesi email: ")
        hash = input("Unesi hash: ")

        new_pass = input("Unesi novu lozinku: ")
        new_pass_again = input("Potvrdi novu lozinku: ")

        if (new_pass != new_pass_again):
            print("Nove lozinke se ne podudaraju.")
            return

        self.cur.execute("SELECT uid FROM users WHERE email=?", (email, ))
        row = self.cur.fetchone()
        
        if(row == None):
            print("Korisnik nije pronađen!")
            return

        uid = row[0]

            # work on this

        self.cur.execute("UPDATE users SET password=? WHERE id=?", (new_pass, uid))

        self.cur.execute("SELECT id, hash FROM forgot_password WHERE uid=?", (uid, ))

        hash_id=0
        self.cur.execute("DELETE FROM forgot_password WHERE id=?", (hash_id))
        self.con.commit()


if __name__=="__main__":
    print("Dobrodošli u Unidu sustav!")
    print("Za prijavu upišite broj 1, za registraciju broj 2, za zaboravljenu lozinku broj 3:")

    unos = 0
    acceptable = [1,2,3]

    while(unos not in acceptable):
        unos = int(input("Unesite broj: "))

    acc = Account()

    if(unos==1):
        acc.login()
    if(unos==2):
        acc.registracija()
    if(unos==3):
        acc.forgot_password()