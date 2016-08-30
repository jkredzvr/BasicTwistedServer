import xmlrpclib  #XML library to encode our remote commands to execute server commands
import sys 
import time
import select

'''
Basic Command line interface for sending Remote Procedure Calls (RPC) commands to
Twisted server on a separate local proxy port.
Proxy port is defined in the server script.
Extensible by adding additional CLI commands mapped to server RPC commands.
'''

proxy = xmlrpclib.ServerProxy("http://localhost:8004") #connect to servery proxy port set up in twisted_server_template

print "Server control initialized"

def getInput():
	while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
		line = sys.stdin.readline()
		if line: return line
		else: pass
	else: return None
	
while 1:
	if True:
		cmd = getInput()
		if cmd is not None:
			print '----'
			try:
				# Append additional command line -> RPC commands here
				if cmd.startswith('BROADCAST'):  #Broaccast a message to all server clients
					proxy.broadcast(cmd[9:])
			except Exception, e:
				print e
	time.sleep(0.25)
					