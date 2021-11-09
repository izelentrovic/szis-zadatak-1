import sqlite3
import time

def main():
    print("Dobrodošli u Unidu sustav!")
    print("Za prijavu upišite broj 1, za registraciju broj 2:")

    unos = 0

    while(unos!=1 and unos!=2):
        unos = int(input("Unesite broj: "))

    email = input("Unesi email: ")
    password = hash_pass(input("Unesi lozinku: "))
    
    if unos == 2:
        name = input("Unesi ime: ")
        contact = input("Unesi kontakt broj: ")
    
        register_user(name, email, password, contact)

def register_user(name, email, password, contact):
    created_at = int(time.time())
    cur.execute("""INSERT INTO user (name, email, password, contact, created_at)
                    VALUES (?, ?, ?, ?, ?)""", (name, email, password, contact, created_at))
    con.commit()

def hash_pass(password):    # implement this
    return password

if __name__=="__main__":
    con = sqlite3.connect('baza.db')
    cur = con.cursor()
    main()