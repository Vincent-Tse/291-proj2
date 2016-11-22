import sqlite3
import os


def main():
    #Do we have to error check the database name?
    database =raw_input("Enter the name of the database: ")
    conn = sqlite3.connect(database)
    c = conn.cursor()
    clearScreen()
    while True:
        print("""Make Selection\n
1) 3NF schema
2) BCNF schema
3)Exit""")
        try:
            print("-"*30)
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

    fds = readInputRelation(conn)
    while len(fds[0]) != 2:
        clearScreen()
        fds = readInputRelation(conn)
    fds = singleRHS(fds)
    #print(fds)


def singleRHS(fds):
    for i in range(len(fds)):
        fd = fds[i]
        if ',' in fd[1]:
            fd[1]=fd[1].split(',')
    #print(fds)
    return fds
def eliminRedundantLHS(conn,fds):
    for fd in fds:
        x=fd[0]
        y=fd[1]
        if len(X) >1:
            for singleX in x:
                if attrClos(conn,singleX) == attrClos(conn,x):
                    fd[0] = singleX


def BCNF(conn):
    readInputRelation(conn)
    pass
def attrClos(conn,closure):
    #closure = raw_input("attribute: ")
    #print(closure)
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
    return closure





def attrEquivalence():
    pass

def readInputRelation(conn):
    c = conn.cursor()
    menu=[]
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    rows=c.fetchall()
    while True:
        print("Make selection")
        print
        for i in range(len(rows)):
            for item in rows[i]:
                item =item.encode("utf-8")
                choice =str(i+1)+')'+item
                print(choice)
                menu.append(item)
        try:
            print("-"*30)
            selection = int(raw_input("Selection: "))
            if selection >len(rows)+1 or selection<1:
                raise
        except:
            clearScreen()
            print("Invalid Input")
            raw_input("")
            continue    # not an integer
        else:
            break
    c.execute("SELECT * FROM "+menu[selection-1]+";")
    rows = c.fetchall()

    table =[]
    for row in rows:
        line=[]
        for i in range(len(row)):
            if type(row[i]) == unicode:
                data = row[i].encode("utf-8")
            else:
                data = row[i]
            line.append(data)
        table.append(line)
    conn.commit()
    return table


def clearScreen():
    os.system("clear")
main()
