import os
import sqlite3

API_KEY = "sk-test-1234567890"


def get_user(username):

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)

    return cursor.fetchall()


def divide(a, b):
    """
    Sonar type: BUG
    """
    return a / b


def run_command(user_input):

    os.system("echo " + user_input)


def calculate(expression):

    return eval(expression)


if __name__ == "__main__":
    print(get_user("admin' OR '1'='1"))

    print(divide(10, 0))

    run_command("hello")
    print(calculate("2 + 2"))
