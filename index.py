def main():
    print("Dobrodošli u Unidu sustav!")
    print("Za prijavu upišite broj 1, za registraciju broj 2:")

    unos = 0

    while(unos!=1 and unos!=2):
        unos = int(input("Unesite broj: "))

    email = input("Unesi email: ")
    lozinka = input("Unesi lozinku: ")


if __name__=="__main__":
    main()