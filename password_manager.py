import sqlite3
import base64
import random
import string
import numpy as np
import datetime
import getpass

PASSWORD = "123456"

connect = input("What is your password?\n")

while connect != PASSWORD:
    connect = getpass("What is your password?\n")
    if connect == "q":
        break


cur = sqlite3.connect("safe.db")
conn = cur.cursor()
try:
    conn.execute(
        '''CREATE TABLE PASSWORD_MANAGER
        (ID INT NOT NULL AUTO_INCREMENT, 
        FULL_NAME TEXT PRIMARY KEY NOT NULL,
        PASSWORD TEXT NOT NULL,
        DATE_CREATED DATE NOT NULL)'''
    )
    print("Your safe has been created!\nWhat would you like to store in it today?")
except:
    print("You already have a safe.\nWhat would you like to store in it today?")

while True:
    print("*"*15)
    print("COMMANDS: ")
    print("q = quit the program")
    print("gp = get all passwords")
    print("sp = store a password")
    print("*"*15)
    input_ = input("->")

    if input_ == "q":
        break
    if input_ == "gp":
        #see password
        results = conn.execute("SELECT * FROM PASSWORD_MANAGER").fetchall()
        if len(results) == 0:
            print("Nothing")
        else:
            for (name, passwrd, date) in results:
                print("Name: "+ name)
                print("Password: "+ passwrd)
                print("Date: "+ date)
        break
    if input_ == "sp":
        branch = input("Name:\n")
        alphabet_string = string.ascii_lowercase
        numeric_number = list(alphabet_string)
        for n in range(1, 100):
            numeric_number.append(str(n))
        tableau = np.concatenate((list(alphabet_string), numeric_number, list(string.ascii_uppercase)))
        value_random = random.choices(tableau, k = 10)
        password = ''.join(map(str, value_random))
        date_now = datetime.datetime.today()
        verify = conn.execute("SELECT * FROM PASSWORD_MANAGER WHERE FULL_NAME=:branch", {"branch": branch})
        if len(verify) == 0:
            conn.execute("INSERT INTO PASSWORD_MANAGER(FULL_NAME, PASSWORD, DATE_CREATED) VALUES (?, ?, ?)", (branch, password, date_now))
            results = conn.execute("SELECT * FROM PASSWORD_MANAGER WHERE FULL_NAME=:branch", {"branch": branch})
            for (name, passwrd, date) in results:
                print("Name: "+ name)
                print("Password: "+ passwrd)
                print("Date: "+ date)
        else:
            print("Already Exist")
            for (name, passwrd, date) in verify:
                print("Name: "+ name)
                print("Password: "+ passwrd)
                print("Date: "+ date)
            
        break
        

