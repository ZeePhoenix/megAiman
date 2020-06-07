import socket
import json
import time
import numpy as np

bizhawk = None
HOST, PORT = "192.168.1.133", 8852

class Server:
	serverLoop = None

	@classmethod
	def awaitConnection(self):
		global bizhawk
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind((HOST, PORT))
		s.listen(15)
		s.setblocking(1)
		print("Awaiting connection from emulator...")
		bizhawk, addr = s.accept()
		bizhawk.setblocking(1)
		bizhawk.settimeout(5)
		print("Connected to Emulator! ", addr)
		Server.serverLoop = Server.startServerLoop()

	@classmethod
	def serverLoop(self):
		romName = (bizhawk.recv(48)).decode('utf-8')
		print("Playing: ", romName)
		while True:
			try:
				# Get our training data from bizhawk
				X = (bizhawk.recv(512)).decode('utf-8')
				print(X)
				# Evaluate our Training Data
				# Send the evaluated Joypad Data to bizhawk
				pass
			except socket.timeout:
				pass
			time.sleep(0.01)

	@classmethod
	def startServerLoop(self):
		t = threading.Thread(target = Server.serverLoop)
		t.daemon = True
		t.start()
		return t

Server.awaitConnection()
while True:
	time.sleep(60)
	pass