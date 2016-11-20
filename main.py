import sqlite3
import os


def main():
    database =raw_input("Enter the name of the database: ")
    conn = sqlite3.connect(database)
    c = conn.cursor()
    clearScreen()
    while True:
        print("""Make Selection\n
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
    c = conn.cursor()

    c.execute("select * from Input_FDs_R1") #HELP!!!! I can't generalize to all table
    relation = c.fetchall()

    closure = raw_input("The attribute :")
    for dependency in relation:
        RHS = dependency[0]
        LHS = dependency[1]
        if RHS in closure:
            for char in LHS:
                if char not in closure:
                    closure+=char
    print(closure)
    conn.commit()

def attrequivalence():
    pass
def clearScreen():
    os.system("clear")
main()
