import socket

VERSION = 1.0

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 12345

client_socket.connect((host, port))

print(f"HR System {VERSION}")

while True:
    while True:
        emp_id = input("Please Enter Employee ID (Or enter 0 for logs) ")
        if emp_id == "":
            print("Please enter a valid id. ")
        else:
            break

    client_socket.send(emp_id.upper().strip().encode())

    response = client_socket.recv(1024).decode()
    if response == "True":
        print(f"Found User: {emp_id} ")
        break
    elif response == "False":
        print(f"No User found with id: {emp_id} ")
        print("Please enter a valid id ")
    else:
        print(f"{response} ")

while True:
    query = ""

    while True:
        option1 = input("Salary (C) or Annual Leave (L)? ")

        if option1.upper().strip() == "C" or option1.upper().strip() == "L":
            break
        else:
            print("Please enter a valid option ")

    query += option1

    if option1.upper().strip() == "C":
        while True:
            option2 = input("Current Salary (S) or Total Salary (T) for year? ")

            if option2.upper().strip() == "S" or option2.upper().strip() == "T":
                break
            else:
                print("Please enter a valid option ")

        query += "," + option2

    client_socket.send(query.upper().strip().encode())

    response = client_socket.recv(1024).decode()
    print(f"Server response: {response}")

    while True:
        sentinel = input("Do you want to continue? (Y/N) ").upper()
        if sentinel.upper().strip() == "Y" or sentinel.upper().strip() == "YES" or sentinel.upper().strip() == "N" \
                or sentinel.upper().strip() == "NO":
            break
        else:
            print("Please enter a valid option ")

    if sentinel.upper().strip() == "N" or sentinel.upper().strip() == "NO":
        break

query = "exit"
client_socket.send(query.encode())
client_socket.close()
