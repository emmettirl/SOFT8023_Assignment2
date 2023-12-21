import socket
import threading
import pika


def handle_client(client_socket, addr):
    employee_list = ["E00123", "E00456", "E00789"]

    print(f"Got a connection from {addr}")

    # Setup RabbitMQ Connection
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare a queue
    channel.queue_declare(queue='employee_id_queue')

    while True:
        # receive and process employee id
        user_input = client_socket.recv(1024).decode()

        if user_input == "0":
            response = read_file_contents("employee_data_access_log.txt")
            client_socket.send(response.encode())


        if user_input not in employee_list:
            response = "False"
            client_socket.send(response.encode())
        else:
            response = "True"
            client_socket.send(response.encode())

            break

    while True:
        command = client_socket.recv(1024).decode()
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

        # Send message to RabbitMQ
        channel.basic_publish(exchange='',
                              routing_key='employee_data_access_log',
                              body=user_input + ", " + str(addr) + ", " + command)
        print(f"Sent {user_input} to RabbitMQ")

        client_socket.send(response.encode())

    # Close the connection
    client_socket.close()


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

    print("Starting to consume from the queue. To exit press CTRL+C")
    channel.start_consuming()


# Server setup
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'  # Localhost
port = 12345
server_socket.bind((host, port))
server_socket.listen(5)

print(f"Server listening on {host}:{port}")

consumer_thread = threading.Thread(target=consume_queue)
consumer_thread.start()

while True:
    # Accept a connection
    client_socket, addr = server_socket.accept()

    # Create a new thread that will handle the client
    client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
    client_thread.start()
