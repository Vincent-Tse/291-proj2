import sqlite3
import os


def main():
    database =raw_input("Enter the name of the database: ")
    conn = sqlite3.connect(database)
    c = conn.cursor()
    clearScreen()
    while True:
        print("""Make Selection
1) 3NF schema
2) BCNF schma
3)Exit\n""")
        try:
            selection = int(raw_input("Selection: "))
            if selection not in (1, 2,3):
                raise
        except:
            clearScreen()
            print("Invalid Input")
            raw_input("")
            continue    # not an integer

        if selection == 1:
            clearScreen()
            thirdNF(conn)
            return

        elif selection == 2:
            clearScreen()
            BCNF(conn)
            return


def thirdNF(conn):
    pass
def BCNF(conn):
    pass
def attrClos():
    pass
def attrequivalence():
    pass
def clearScreen():
    os.system("clear")
main()
