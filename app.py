import os
import sqlite3

API_KEY = "sk-test-1234567890"

def get_user(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)

    return cursor.fetchall()


def run_command(user_input):
    os.system("echo " + user_input)


def calculate(expression):
    return eval(expression)


def divide(a, b):
    return a / b


if __name__ == "__main__":
    name = input("Enter username: ")
    print(get_user(name))

    cmd = input("Enter command: ")
    run_command(cmd)

    exp = input("Enter math expression: ")
    print(calculate(exp))

    print(divide(10, 0))
