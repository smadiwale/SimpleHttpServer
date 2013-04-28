import socket
from server_constants import *



class HttpServer:
	def __init__(self):
		self.acceptingConnections = True
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.bind(('', SERVER_HTTP_PORT))
		self.sock.listen(SERVER_LISTEN_BACKLOG)
		self.numConnections=0
		
	#Revisit this 
	def stop(self):
		self.acceptingConnections = False

	def isAcceptingConnections(self):
		if self.numConnections ==3:
			print "Max Connections reached"
			return False
		else:
			return True

	def start(self):
		while self.isAcceptingConnections():
			if self.sock:
				print "Accepting Connections..."
				(remoteSock, address ) = self.sock.accept()
				if (remoteSock):
					self.processConnection(remoteSock, address)
				else:
					print "Error: Invalid Remote socket"
					remoteSock.close()
					return SERVER_ERR_REMOTE_SOCK_INVALID

			else:
				return SERVER_ERR_SERV_SOCK_INVALID

		self.sock.close()
	


	def processConnection(self, remoteSock, remoteAddress):
		print "Recd: sock: %s addr:%s"  % (str(remoteSock), str(remoteAddress)) 	
		remoteSock.close()
		self.numConnections+=1

if __name__ == "__main__":
	server = HttpServer()
	server.start()
	
