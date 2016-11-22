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
    fds = eliminRedundantLHS(fds)
    #print(fds)
    eliminRedundantRHS(fds)

    #print(fds)


def singleRHS(fds):
    newfds=[]
    for i in range(len(fds)):
        fd = fds[i]
        fds[i][0] = fds[i][0].replace(",",'')
        fds[i][1] = fds[i][1].replace(",",'')
        if len(fd[1]) >1:
            for j in range(len(fd[1])):
                newfds.append([fd[0],fd[1][j]])
        else:
            newfds.append(fd)

    return newfds

def eliminRedundantLHS(fds):
    for i in range(len(fds)):
        fd = fds[i]
        cont = True
        while cont:
            x=fd[0]
            y=fd[1]

            if len(x) <= 1:
                cont = False
            old = x
            for singleX in x:
                new = old
                if attrClos(fds,x.replace(singleX,'')) == attrClos(fds,x):
                    #bGH+ = BGHEF and #BH+ = BHEF can I delete bGH -> F?
                    fds[i][0] = x.replace(singleX,'')
                    new = x.replace(singleX,'')
                new = old
            if old == new:
                cont = False
    return fds

def eliminRedundantRHS(fds):#Infinite Loop!!!!!!!
    print(fds)
    cont = True
    new = []
    while cont:
        new = []
        change = False

        for i in range(len(fds)):
            line =[]
            for j in range(len(fds[i])):
                line.append(fds[i][j])
            new.append(line)
        for k in range(len(fds)):
            x = fds[k][0]
            cont = True
            diff =new.pop(0)
            print("old",fds)
            print("new:",new)
            print(attrClos(fds,x))
            print(attrClos(new,x))
            print("")
            if attrClos(fds,x) == attrClos(new,x):
                fds = new
                change = True
            else:
                for i in range(len(fds)):
                    line =[]
                    for j in range(len(fds[i])):
                        line.append(fds[i][j])
                    new.append(line)
        if not change:###
            cont = False
    print(fds)

def BCNF(conn):
    readInputRelation(conn)
    pass
def attrClos(fds,closure):
    #closure = raw_input("attribute: ")
    #print(closure)
    closure = closure.replace(',','')
    while True:
        old = closure
        for dependency in fds:
            LHS = dependency[0]
            RHS = dependency[1]
            if ',' in LHS:
                LHS = "".join(dependency[0].replace(',',''))
            if ',' in RHS:
                RHS = "".join(dependency[1].replace(',',''))
            if all(char in closure for char in LHS) and not any(letter in closure for letter in RHS):
                closure+=RHS
        if old == closure:
            break
    return sorted(closure)





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
