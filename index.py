import hashlib
import sqlite3
from datetime import date
con = sqlite3.connect('baza.db')


def login():
        ime = input("Unesi ime: ")
        lozinka = input("Unesi lozinku: ")
        
        cur = con.cursor()
        password=cur.execute("SELECT password FROM users WHERE name = ?", (ime,))
        password=cur.fetchone()
        print(password)
        if(cur.rowcount>0):
                print("Korisnik postoji \n")

        
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
        

def main():
    print("Dobrodošli u Unidu sustav!")
    print("Za prijavu upišite broj 1, za registraciju broj 2:")

    unos = 0

    while(unos!=1 and unos!=2):
        unos = int(input("Unesite broj: "))


    if(unos==2):
        registracija()
        
    if(unos==1):
        login()


if __name__=="__main__":
    main()