import socket
import sys

HEADER_MSG_LEN = 64
MSG_FORMAT = "utf-8"
PORT = 5050
DISCONNECT_MSG = "!DISCONNECT"
HOSTNAME = socket.gethostname()
SERVER = socket.gethostbyname(HOSTNAME)
ADDRESS = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)

def send(msg):
	message = msg.encode(MSG_FORMAT)
	msg_length = str(len(message)).encode(MSG_FORMAT)
	send_length = msg_length + b' ' * (HEADER_MSG_LEN - len(msg_length))
	client.send(send_length)
	client.send(message)
	print(client.recv(2048).decode(MSG_FORMAT))

while True:
	IN = input()
	send(IN)
	if IN == DISCONNECT_MSG:
		sys.exit()
send(DISCONNECT_MSG)