import sqlite3

def main():
    database =raw_input("Enter the name of the database")
    conn = sqlite3.connect(database)
    
main()
