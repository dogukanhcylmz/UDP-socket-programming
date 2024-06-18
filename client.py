import socket

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5000
RESPONSE_SIZE = 1024

client_port = int(input("Enter the client port number: "))

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.bind((SERVER_IP, client_port))

try:
    while True:  
        message = input("Enter a message: ")
        if message.lower() == "exit": 
            print("Exiting client.")
            break

        client_socket.sendto(message.encode(), (SERVER_IP, SERVER_PORT))

        response, _ = client_socket.recvfrom(RESPONSE_SIZE)
        print(response.decode())

        if response.decode() == "Port is not allowed to communicate":
            break
finally:
    client_socket.close()
