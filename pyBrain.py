import socket
import json
import time
import threading
import numpy as np

bizhawk = None
HOST, PORT = "192.168.1.133", 8852

Brain = []

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
		pass

	@classmethod
	def startServerLoop(self):
		t = threading.Thread(target = Server.serverLoop)
		t.daemon = True
		t.start()
		return t

	@classmethod
	def serverLoop(self):
		romName = (bizhawk.recv(48)).decode('utf-8')
		print("Playing: ", romName)
		Network.initalizeNetwork()
		while True:
			try:
				# Get our training data from bizhawk
				X = [123,0,1,24,20] #Temp Data
				# Evaluate our Training Data
				print(Network.feedForward(X))
				# Send the evaluated Joypad Data to bizhawk
				pass
			except socket.timeout:
				pass
			time.sleep(0.01)
		pass


class Layer_Dense:
	def __init__(self, inputs, neurons):
		self.weights = 0.1 * np.random.randn(inputs, neurons)
		self.biases = np.full((1, neurons), 0.0)
		pass
	def forward(self, inputs):
		self.output = np.dot(inputs, self.weights) + self.biases
		pass

class Network:
	global Brain

	@classmethod
	def initalizeNetwork(self):
		# Creates our Neural Network with 2 Hidden Layers
		# Input layer
		Brain.append(Layer_Dense(5,8))
		# Hidden Layers
		Brain.append(Layer_Dense(8,8))
		Brain.append(Layer_Dense(8,8))
		# Output Layer - Gives our joypad signal
		Brain.append(Layer_Dense(8,6))
		pass
	@classmethod
	def feedForward(self, X):
		Brain[0].forward(X)
		Brain[1].forward(Brain[0].output)
		Brain[2].forward(Brain[1].output)
		Brain[3].forward(Brain[2].output)
		return Brain[3].output



Server.awaitConnection()
while True:
	time.sleep(60)
	pass