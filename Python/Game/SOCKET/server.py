import socket
import threading

HEADER_MSG_LEN = 64
MSG_FORMAT = "utf-8"
PORT = 5050
HOSTNAME = socket.gethostname()
SERVER = socket.gethostbyname(HOSTNAME)
ADDRESS = (SERVER, PORT)
DISCONNECT_MSG = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)

def handle_client(connection, address):
	print(f"[NEW CONNECTION] {address} connected.")

	connected = True
	while connected:
		header_message = connection.recv(HEADER_MSG_LEN).decode(MSG_FORMAT)
		if header_message:
			header_message = int(header_message)
			body_message = connection.recv(header_message).decode(MSG_FORMAT)
			if body_message == DISCONNECT_MSG:
				connected = False
			print(f"[{address}] {body_message}")
			connection.send("message received".encode(MSG_FORMAT))
	connection.close()

def start():
	server.listen()
	print(f"[LISTENING] Server is listening on {SERVER}")
	while True:
		connection, address = server.accept()
		thread = threading.Thread(target = handle_client, args = (connection, address))
		thread.start()
		print(f'[ACTIVE CONNECTIONS] {threading.activeCount() - 1}')

print("[STARTING] server is starting...")
start()