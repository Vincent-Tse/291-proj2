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
        else:
            return


def thirdNF(conn):
    readInputRelation(conn)
    pass
def BCNF(conn):
    readInputRelation(conn)
    pass
def attrClos(conn):

    closure = raw_input("attribute: ")
    print(closure)
    relation = readInputRelation(conn)
    while True:
        old = closure
        for dependency in relation:
            LHS = "".join(dependency[0].split(","))
            RHS = "".join(dependency[1].split(","))
            if all(char in closure for char in LHS) and not any(letter in closure for letter in RHS):
                closure+=RHS
        if old == closure:
            break
    print(closure)
    conn.commit()




def attrEquivalence():
    pass

def readInputRelation(conn):
    c = conn.cursor()
    FDlist =[]
    menu=[]
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    rows=c.fetchall()
    for i in range(len(rows)):
        for item in rows[i]:
            print(i,item)
            menu.append(item)
    #c.execute("SELECT * FROM "+menu[i-1]+";")
    relation = c.fetchall()

    for row in relation:
        FDlist.append([row[0].encode("utf-8"),row[1].encode("utf-8")])
    return(FDlist)

def clearScreen():
    os.system("clear")
main()
