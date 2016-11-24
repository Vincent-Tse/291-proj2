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
    print("Input the relation of the function Dependency")
    fds = readInputRelation(conn)
    while len(fds[0]) != 2:
        clearScreen()
        print("Input the relation of the function Dependency")
        fds = readInputRelation(conn)

    fds = singleRHS(fds)
    #print(fds)
    fds = eliminRedundantLHS(fds)
    #print(fds)
    fds = eliminRedundantRHS(fds)
    fds = mergeLHS(fds)
    schemas = fdsToSchema(fds,conn)
    choice = ''
    while choice not in ('y','n'):
        try:
            choice = raw_input("Generate relation in 3NF schema?(Y/N)").lower()
        except:
            pass

    if choice == 'y':
        generateRelation(schemas,fds,conn)
    else:
        return


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

def eliminRedundantRHS(fds):
    print(fds)
    new = []

    for k in range(len(fds)):
        new = []
        for i in range(len(fds)):
            line =[]
            for j in range(len(fds[i])):
                line.append(fds[i][j])
            new.append(line)
        if k<= i:
            x = fds[k][0]
            cont = True
            diff =new.pop(k)
            if attrClos(fds,x) == attrClos(new,x) and fds != new:
                fds = new


        if k == i:
            break
    return fds

def mergeLHS(fds):
    new = []
    for i in range(len(fds)):
        for j in range(i+1,len(fds)):
            if fds[i][0] == fds[j][0]:
                fds[i][1]+= fds[j][1]
            fds[i][1]="".join(sorted(fds[i][1]))
        add = False
        if all(fds[i][0] != new[k][0] for k in range(len(new))):
            new.append(fds[i])

    return new

def fdsToSchema(fds,conn):
    global outputPrefix
    schemas =[]
    clearScreen()
    print("Schema:")
    print("="*30)
    c = conn.cursor()
    prefix = 'Input_FDS_R%'
    c.execute("SELECT name FROM sqlite_master WHERE name like 'Input_FDs_R%';")
    rows=c.fetchall()
    name =rows[0][0].encode("utf-8")

    outputPrefix = name.replace("In","Out")+'_'

    fdSchemas = []
    relationSchemas =[]
    coverAttr = ''
    for fd in fds:
        fdschema = outputPrefix+''.join(fd)
        relationSchema = fdschema.replace("_FDs",'')
        fdSchemas.append(fdschema)
        relationSchemas.append(relationSchema)
        coverAttr +=''.join(set(fd))
    coverAttr = ''.join(set(coverAttr))
    ###########################################
    c.execute("SELECT * from "+name+";")
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
    allAttr = ''
    for fd in table:
        for side in fd:
            allAttr += side
    allAttr = allAttr.replace(",","")
    allAttr = "".join(set(allAttr))
    ##########################################
    diff = ""
    for char in allAttr:
        if char not in coverAttr:
            diff += char

    c.execute("SELECT * from "+name+";")
    rows = c.fetchall()
    for row in rows:
        for i in range(2):
            if diff in row[i]:
                missing = row[i].encode("utf-8").replace(",","")
                missingSchema = outputPrefix.replace("_FDs","")+missing
                relationSchemas.append(missingSchema)
    schemas.append(fdSchemas)
    schemas.append(relationSchemas)

    for types in schemas:
        for schema in types:
            print (schema)
    return schemas

def generateRelation(schemas,fds,conn):
    c = conn.cursor()
    #create table for function dependency
    for i in range(len(schemas[0])):
        c.execute("DROP table if exists "+ schemas[0][i] + ";")
        command = "create table "+schemas[0][i]+"( LHS TEXT,RHS TEXT);"
        c.execute(command)
        conn.commit()
        command = "insert into "+schemas[0][i] +" values( '"+fds[i][0]+"','"+fds[i][1]+"' );"
        c.execute(command)
        conn.commit()
    #create table for data
    c.execute("SELECT * from sqlite_master WHERE name like 'Input_R%'")
    rows = c.fetchall()
    createCommand = rows[0][4].encode("utf-8")
    originalName = rows[0][1].encode("utf-8")
    print(originalName)
    for i in range(len(schemas[1])):
        attr = schemas[1][i].replace(outputPrefix.replace("_FDs",''),'')
        c.execute("DROP table if exists "+ schemas[1][i] + ";")
        individualCreateCommand =createCommand.replace(originalName,schemas[1][i])
        individualCreateCommand =individualCreateCommand.split('\n')
        remove=[]

        l = 0
        for line in individualCreateCommand:
            if l not in (0,len(individualCreateCommand)-1):
                if all(char not in line[2] for char in attr):
                    remove.append(line)
            l+=1
        for item in remove:
            individualCreateCommand.remove(item)

        if  ',' in individualCreateCommand[-2]:
            individualCreateCommand[-2] =individualCreateCommand[-2].replace(',','')

        individualCreateCommand =''.join(individualCreateCommand).replace(";",'')
        for j in range(len(fds)):
            fd = fds[j]
            if all(char in fd[0] or char in fd[1] for char in attr):
                pk = fd[0]
                break
            else:
                if j == len(fd)-1:
                    pk = ''
        if pk != '':
            key = "\nPRIMARY KEY "
            key+= '('
            for k in range(len(pk)):
                key +="'"+pk[k]+"'"
                if  k != len(fd)-1 and len(pk) != 1:
                    key += ','
            key+= ')'
            individualCreateCommand =''.join(individualCreateCommand)+','
            individualCreateCommand =individualCreateCommand.replace(')','')+key+'\n);'
        c.execute(individualCreateCommand)
        conn.commit()
        #fill table with data

        value =''
        print(attr)
        if pk != '':
            for m in range(len(pk)):
                value += attr[m]
                if  m != len(pk)-1 and len(pk) != 1:
                    value += ','
                print (value)
            fillDataCommand = "insert into "+schemas[1][i] +"("+value+")\n"
            fillDataCommand +="SELECT Distinct "+value+" FROM "+originalName+";"
            print(fillDataCommand)
            c.execute(fillDataCommand)
        conn.commit()
#########################################################################################
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
