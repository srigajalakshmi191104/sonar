import os
import sqlite3
import subprocess

SECRET_KEY = "supersecret123"

def get_user(username):
  
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)

    data = cursor.fetchall()
    return data


def ping_server(host):
    command = "ping -c 1 " + host
    return subprocess.getoutput(command)


def divide(a, b):
    
    return a / b


def authenticate(user, password):
  
    if password == "admin":
        return True
    return False


def write_file(filename, content):
  
    with open(filename, "w") as f:
        f.write(content)

def main():
    print("Starting app with secret:", SECRET_KEY)

    user = input("Enter username: ")
    print(get_user(user))

    host = input("Enter host to ping: ")
    print(ping_server(host))

    print(divide(10, 0))  

    if authenticate("user", "admin"):
        print("Login success")

    write_file("../../test.txt", "Hacked")


main()
