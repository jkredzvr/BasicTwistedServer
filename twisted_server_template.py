import twisted.internet #provides twisted reactor, could do from twisted.internet import reactor instead
import autobahn.twisted.websocket   #provides twisted ws instructions for factory, from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol
import uuid, json  #for identification and msg parsing
import twisted.web.xmlrpc  #enables XML_RPC commands over TCP  
import twisted.web.server

#override twisted factory class
class ServerFactory(autobahn.twisted.websocket.WebSocketServerFactory):
    def __init__(self, *args, **kwargs):
    	#retain parent factory class' method
    	super(autobahn.twisted.websocket.WebSocketServerFactory,self).__init__(*args, **kwargs)
        
    	#dictionaries for managing clients and client UUID 
        self.clients = {}   # session_id has clients of "Unity, Phone, etc"
        self.client_identities = {}  #client_id # belongs to session_id #

    # reistration method    
	def register(self, client, session_id, identity):
		# if session_id is not a key in client's dictionary
		if not session_id in self.clients:
			#update clients dictionary with session:client - this session has this Twisted client "Unity, Phone, etc..."
			self.clients.update({session_id:client})
			#update client identities dictionary with the identity:session_id - this client idenity belongs to this session
			self.client_identities.update({identity:session_id})
	
	def unregister(self, client, session_id, identity):
		if session_id in self.clients:
			#remove the session_id from clients dictionary
			self.clients.pop(session_id)
		if identity is not None: 
			#remove the identity from client_identities dictionary
			self.client_identities.pop(identity)

	def broadcast(self, msg):
		#.items() returns tuple of registered client's dict key:value pairs
		#for each returned tuple
		for session_id, client in self.clients.items():
			# call each clients sendMessage method
			client.sendMessage(msg)

#protocol to handle clients
class ServerProtocol(autobahn.twisted.websocket.WebSocketServerProtocol):
    def __init__(self, *args, **kwargs):
    	super(autobahn.twisted.websocket.WebSocketServerProtocol,self).__init__(*args, **kwargs)

    	#every client has identity, session_id, client_type, and identified properites
        self.identity = None  		#identity assigned from client device (Unity) 
        self.identified = False
        self.session_id = uuid.uuid4()  #identity uuid assigned within the server 
        self.client_type = None

    # clients can call this onMessage method
	def onMessage(self, msg, isBinary):
		try:
			msg = json.loads(msg)[0]
		except:
			print "Message not JSON formatted string"
			return

		if not self.identified:
			try:
				 self.identity = msg.get('proto').get('identity')
				 self.client_type = msg.get('proto').get('type')
				 #register client to factory
				 self.factory.register(self,self.session_id,self.identity)
				 self.identified = True
			except Exception,e:
				 print "Not identified:", e

class Interface(twisted.web.xmlrpc.XMLRPC):
	#xmlrpc commands must start wtih xmlrpc_ ......
	def xmlrpc_broadcast(self, msg):
		return factory.broadcast(msg)
 
 #server side
if __name__=='__main__':
    factory = ServerFactory("ws://localhost:9000", debug=False)
    factory.protocol = ServerProtocol
    autobahn.twisted.websocket.listenWS(factory)

    twisted.internet.reactor.listenTCP(8004, twisted.web.server.Site(Interface()))  #Server is listening over TCP (port 8004) for XML-RPC commands that we’ve defined in Interface

    print "running"
    twisted.internet.reactor.run()
