import mysql.connector as db_connect
import random
import string
import numpy as np
import datetime
import getpass

mydb = db_connect.connect(
    host="localhost",
    user="root",
    password="",
    database="python_test",
    port= 3306
)

# try:
#     requesting = """
#         CREATE TABLE PASSWORD_MANAGER(
#         ID INT AUTO_INCREMENT PRIMARY KEY, 
#         FULL_NAME VARCHAR(255) NOT NULL, 
#         PASSWORD VARCHAR(255) NOT NULL, 
#         DATE_CREATED DATE NOT NULL)"""
#     mydb.cursor().execute(requesting)
# except:
#     print("Table exist")

date_now = datetime.datetime.today()

def choice():
    print("*"*30)
    print("COMMANDS: ")
    print("q = quit the program")
    print("gp = get all passwords")
    print("sp = store a password")
    print("cp = change password")
    print("*"*30)

def continue_choice():
    print("*"*30)
    next_move = input("Do you want to continue? Y/N\n")
    return next_move.lower()

def newGenerate():
    alphabet_string = string.ascii_lowercase
    numeric_number = list(alphabet_string)
    for n in range(1, 100):
        numeric_number.append(str(n))
    tableau = np.concatenate((list(alphabet_string), numeric_number, list(string.ascii_uppercase)))
    value_random = random.choices(tableau, k = 10)
    password = ''.join(map(str, value_random))
    return password

def main_logic():
    while True:
        choice()
        input_ = input("->")

        if input_ == "q":
            break
        if input_ == "gp":
            #see password
            mycursor = mydb.cursor()
            mycursor.execute("SELECT * FROM PASSWORD_MANAGER")
            results = mycursor.fetchall()
            if len(results) == 0:
                print("Nothing")
            else:
                for (id, name, passwrd, date) in results:
                    print("*"*30)
                    print("Name: "+ name)
                    print("Password: "+ passwrd)
                    print("Date: "+ str(date))
            next_move = continue_choice()
            if next_move == "y":
                main_logic()
            elif next_move == "n":
                break
        if input_ == "sp":
            branch = input("Name:\n")
            password = newGenerate()
            cursor = mydb.cursor()
            cursor.execute("SELECT * FROM PASSWORD_MANAGER WHERE FULL_NAME = %s", (branch, ))
            verify = cursor.fetchall()
            if len(verify) == 0:
                cursor.execute("INSERT INTO PASSWORD_MANAGER (FULL_NAME, PASSWORD, DATE_CREATED) VALUES (%s, %s, %s)", (branch, password, date_now))
                mydb.commit()
                cursor.execute("SELECT * FROM PASSWORD_MANAGER WHERE FULL_NAME = %s", (branch, ))
                results = cursor.fetchall()
                for (id, name, passwrd, date) in results:
                    print("*"*30)
                    print("Name: "+ name)
                    print("Password: "+ passwrd)
                    print("Date: "+ str(date))
            else:
                print("Already Exist")
                for (id, name, passwrd, date) in verify:
                    print("*"*30)
                    print("Name: "+ name)
                    print("Password: "+ passwrd)
                    print("Date: "+ str(date))
            next_move = continue_choice()
            if next_move == "y":
                main_logic()
            elif next_move == "n":
                break
        if input_ == "cp":
            exist_password_name = input("Name: \n")
            cursor = mydb.cursor()
            cursor.execute("SELECT * FROM PASSWORD_MANAGER WHERE FULL_NAME = %s", (exist_password_name, ))
            verify = cursor.fetchone()
            if verify:
                print("*"*30)
                (id, name, password, datePut) = verify

                new_name = input("New name: \n")

                new_password = newGenerate()

                print("Your new password")
                print("-> ", new_password)

                print("*"*30)

                confirm_new = input("Would like you to confirm? Y/N \n")

                if confirm_new.lower() == "y":
                    sql = "UPDATE PASSWORD_MANAGER SET FULL_NAME = %s, PASSWORD = %s, DATE_CREATED = %s WHERE ID = %s"

                    val = (new_name, new_password, date_now, str(id))

                    cursor.execute(sql, val)

                    cursor.execute("INSERT INTO PASSWORD_OLD (FULL_NAME, PASSWORD, DATE_CREATED) VALUES (%s, %s, %s)", (new_name, password, datePut))

                    mydb.commit()
                else:
                    main_logic()

            else:
                print("Don't exist")
                main_logic()

main_logic()