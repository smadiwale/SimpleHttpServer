import socket
import os
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
			print "Max Connections reached. Exiting."
			return False
		else:
			return True

	def start(self):
		r = SERVER_ERR_NONE
		while self.isAcceptingConnections():
			if self.sock:
				print "\nAccepting Connections..."
				(remoteSock, address ) = self.sock.accept()
				if (remoteSock):
					self.processConnection(remoteSock, address)
				else:
					print "Error: Invalid Remote socket"
					remoteSock.close()
					r = SERVER_ERR_REMOTE_SOCK_INVALID

			else:
				r = SERVER_ERR_SERV_SOCK_INVALID

		self.sock.close()
		return r
	


	def processConnection(self, remoteSock, remoteAddress):
		print "Rx: addr:%s"  % (str(remoteAddress), ) 	
		rStr = remoteSock.recv(1000)
		rStr = rStr.split()
		if rStr[0] and rStr[1] and rStr[2]:
			print "Rx:", rStr[0], rStr[1], rStr[2]
			if rStr[0] == "GET":
				#Now return the contents of the directory instead.
				dirList = os.listdir(".")
				remoteSock.send("<HTML>")
				#First transmit the back dir link
				remoteSock.send(SERVER_UP_ONE_DIR_ANCHOR+"<BR>")
				for dirlink in dirList:
					sendStr = "<A href=\"" + dirlink +"\">"+ dirlink + "</A><BR>"
					remoteSock.send(sendStr)
				remoteSock.send("</HTML>")

		remoteSock.close()
		self.numConnections+=1


if __name__ == "__main__":
	server = HttpServer()
	server.start()
	
