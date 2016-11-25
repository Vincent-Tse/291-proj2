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
            if selection not in (1,2,3):
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

def getStartRelation(conn):
    relation = ""
    fds = readInputRelation(conn)
    for fd in fds:
        for side in fd:
            relation += side
    relation = relation.replace(",","")
    relation = "".join(set(relation))
    return relation

def errorCheckFDs(conn):
    newfds = []
    fds = readInputRelation(conn)
    for j in range(len(fds)):
        newfds.append([fds[j][0],fds[j][1]])
        newfds[j][0] = newfds[j][0].split(",")
        newfds[j][1] = newfds[j][1].split(",")
    for i in range(len(newfds)):
        for c in range(len(newfds[i][0])):
            for d in range(len(newfds[i][1])):
                if newfds[i][0][c] == newfds[i][1][d]:
                    newfds[i][1].replace(newfds[i][1][d],"")
    for i in range(len(newfds)):
        newfds[i][0] = "".join(newfds[i][0])
        newfds[i][1] = "".join(newfds[i][1])
    return newfds

def isSuperKey(fds,closure,relation):
    keyrelation = attrClos(fds,closure)
    if sorted(keyrelation) == sorted(relation):
        return True
    else:
        return False

def BCNF(conn):
    startingRelation = getStartRelation(conn)
    fds = errorCheckFDs(conn)
    resultRelations = []
    changefds = []
    for i in fds:
        changefds.append(i)
    for i in range(len(fds)):
        lhs = changefds[i][0]
        rhs = changefds[i][1]
        if not isSuperKey(changefds,lhs,startingRelation):
            resultRelations.append(changefds[i])
            for char in rhs:
                startingRelation = startingRelation.replace(char,"")
                for d in range(i+1,len(fds)):
                    if char in changefds[d][0] or char in changefds[d][1]:
                        changefds[d][0] = changefds[d][0].replace(char,"")
                        changefds[d][1] = changefds[d][1].replace(char,"")
                        for g in range(len(changefds)):
                            if changefds[g][0] == "" or changefds[g][1] == "":
                                changefds[g] = ["",""]
    index = []
    for h in range(len(resultRelations)):
        if "" in resultRelations[h]:
            index.append(h)
    for dex in range(len(index)):
        resultRelations.pop(index[dex]-dex)
    return resultRelations

def attrClos(fds,closure):
    #closure = raw_input("attribute: ")
    #print(closure)
    closure = closure.replace(",","")
    while True:
        old = closure
        for dependency in fds:
            LHS = "".join(dependency[0].replace(",",""))
            RHS = "".join(dependency[1].replace(",",""))
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
