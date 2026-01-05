import os
import subprocess

def insecure_function(user_input):
    # Command Injection (Vulnerability)
    os.system("ls " + user_input)

def hardcoded_password():
    password = "admin123"  # Security issue
    return password

def divide(a, b):
    return a / b  # Possible ZeroDivisionError (Bug)

if __name__ == "__main__":
    insecure_function("; rm -rf /")
    print(hardcoded_password())
    print(divide(10, 0))
