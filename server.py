import socket
import threading
import pika


def handle_client(c_socket, c_addr):
    employee_list = ["E00123", "E00456", "E00789"]

    print(f"Got a connection from {c_addr}")

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='employee_id_queue')

    while True:
        user_input = c_socket.recv(1024).decode()

        if user_input == "0":
            response = read_file_contents("employee_data_access_log.txt")
            c_socket.send(response.encode())

        if user_input not in employee_list:
            response = "False"
            c_socket.send(response.encode())
        else:
            response = "True"
            c_socket.send(response.encode())

            break

    while True:
        command = c_socket.recv(1024).decode()
        print(f"Received command: {command}")

        query = command.split(",")

        if query[0] == "exit":
            break

        if query[0] == "C":
            if query[1] == "S":
                response = "Current Salary: 1000"
            elif query[1] == "T":
                response = "Total Salary: 12000"
        elif query[0] == "L":
            response = "Annual Leave: 14"
        else:
            response = "Invalid Query"

        channel.basic_publish(exchange='',
                              routing_key='employee_data_access_log',
                              body=user_input + ", " + str(c_addr) + ", " + command)
        print(f"Sent {user_input} to RabbitMQ")

        c_socket.send(response.encode())
    c_socket.close()


def append_to_file(message):
    with open("employee_data_access_log.txt", "a") as file:
        file.write(message + "\n")


def read_file_contents(file_path):
    try:
        with open(file_path, "r") as file:
            return file.read()
    except FileNotFoundError:
        return "File not found."


def consume_queue():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='employee_data_access_log')

    def callback(ch, method, properties, body):
        print(f"Received {body.decode()}")
        append_to_file(body.decode())

    channel.basic_consume(queue='employee_data_access_log', on_message_callback=callback, auto_ack=True)

    print("Consuming queue")
    channel.start_consuming()

# server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '0.0.0.0'
port = 12345
server_socket.bind((host, port))
server_socket.listen(5)

print(f"Server listening on {host}:{port}")

consumer_thread = threading.Thread(target=consume_queue)
consumer_thread.start()


#threads
while True:
    client_socket, addr = server_socket.accept()

    client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
    client_thread.start()
