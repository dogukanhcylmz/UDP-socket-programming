import socket
import re

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5000
CLIENT_PORT1 = 1234
CLIENT_PORT2 = 3333

permitted_numbers = []
client_addresses = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((SERVER_IP, SERVER_PORT))

PERMISSION_PATTERN = r"^Permission(\d+)$"
REQUEST_PATTERN = r"Request(\d+)$"

permission_pattern = PERMISSION_PATTERN
request_pattern = REQUEST_PATTERN

response_message = ""

def handle_permission(message):
  match = re.match(PERMISSION_PATTERN, message, re.IGNORECASE)
  if match:
    num = match.group(1)  
    if num in permitted_numbers:
      return "Already Permitted"
    else:
      permitted_numbers.append(num)
      return "Permission Accepted"
  else:
    return "Invalid Message"
    
def handle_request(message):
  match = re.match(REQUEST_PATTERN, message, re.IGNORECASE)
  if match:
    num = match.group(1)
    if num in permitted_numbers:
      return "Request Accepted"
    else:
      return "Request Rejected"
  else:
    return "Invalid Message"

try:
    while True:
        message, client_address = server_socket.recvfrom(1024)
        client_message = message.decode()
        client_ip, client_port = client_address

        print(f"Message: {client_message}")
        print(f"Client Address: ('IP: {client_ip}', Port Number: {client_port})")

        if client_port == CLIENT_PORT1:
            response_message = handle_permission(client_message)
        elif client_port == CLIENT_PORT2:
            response_message = handle_request(client_message)
        elif client_port not in [CLIENT_PORT1, CLIENT_PORT2]:
            response_message = "Port is not allowed to communicate"

        server_socket.sendto(response_message.encode(), client_address)

        client_combo = client_ip + ":" + str(client_port)
        if client_combo not in client_addresses:
            client_addresses.append(client_combo)

        if len(client_addresses) >= 4:
            print("Maximum number of clients reached, server will close.")
            break

finally:
    server_socket.close()
    print("Server is closed")
