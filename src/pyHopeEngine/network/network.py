'''
Created on Aug 5, 2013

@author: Devon

Defines network classes
'''

import socket
import ipaddress
import Mastermind as MM

from pyHopeEngine import engineCommon as ECOM
from pyHopeEngine import Event_ClientConnected, Event_IPInput, Event_IPValid

class Server(MM.MastermindServerTCP):
    '''Main server'''
    
    def __init__(self, timeServerRefresh = 0.5, timeConnectionRefresh = 0.5, timeConnectionTimeout = 5.0):
        '''Create a new server
        
        Keyword arguments:
            timeServerRefresh -- how quickly server checks for end condition
            timeConnectionRefresh -- how long till server checks for end condition
            timeConnectionTimeout -- how long connection can be idle before considered dead
        '''
        
        super().__init__(timeServerRefresh, timeConnectionRefresh, timeConnectionTimeout)
        self.connectionObject = None
    
    def callback_connect_client(self, connection_object):
        '''Called when a client connects'''
        event = Event_ClientConnected()
        ECOM.eventManager.queueEvent(event)
        self.connectionObject = connection_object
        return super().callback_connect_client(connection_object)
    
    def callback_disconnect_client(self, connection_object):
        '''Called when a client disconnects'''
        return super().callback_disconnect_client(connection_object)
    
    def callback_client_receive(self, connection_object):
        '''Called when data about to be recieved'''
        return super().callback_client_receive(connection_object)
    
    def callback_client_handle(self, connection_object, data):
        '''Called to handle the sent data'''
        if data == "update":
            return
        
        for event in data:
            if event is not None:
                ECOM.eventManager.queueEvent(event)
        return super().callback_client_handle(connection_object,data)
    
    def callback_client_send(self, connection_object, data):
        '''Called when data about to be sent to a client'''
        return super().callback_client_send(connection_object, data)
    

class Client(MM.MastermindClientTCP):
    '''Main client'''
    
    def __init__(self, timeoutConnect = None, timeoutRecieve = None):
        '''Creates a new client object
        
        Keyword arguments:
            timeoutConnect -- how long to wait for connection before timing out
            timeoutRecieve -- how long to wait when receiving data
        '''
        
        super().__init__(timeoutConnect, timeoutRecieve)


class NetworkManager(object):
    '''Base class to manage network objects'''
    
    def __init__(self):
        self.type = None
        self.outData = []
        self.ip = None
        self.port = 6317
    
    def init(self):
        raise NotImplementedError("init not implemented.")
    
    def update(self):
        raise NotImplementedError("update not implemented.")
    
    def send(self, data):
        raise NotImplementedError("send not implemented.")
    

class ServerManager(NetworkManager):
    '''Manages the server object'''
    
    def __init__(self):
        super().__init__()
        self.type = "server"
        self.server = None
        self.clients = None
    
    def init(self):
        self.ip = socket.gethostbyname(socket.gethostname())
        self.server = Server()
        self.server.connect(self.ip, self.port)
        self.server.accepting_allow()

    def send(self, data):
        if data == "disconnect":
            self.server.callback_client_send(self.server.connectionObject, data)
        else:
            self.outData.append(data)
        
    def update(self):
        if self.outData:
            self.server.callback_client_send(self.server.connectionObject, self.outData)
            self.outData.clear()

    def cleanUp(self):
        self.server.accepting_disallow()
        if self.clients is not None:
            self.send("disconnect")
        self.server.disconnect_clients()
        self.server.disconnect()
        self.server = None
        

class ClientManager(NetworkManager):
    '''Manages client objects'''
    
    def __init__(self):
        super().__init__()
        self.type = "client"
        self.client = None
        self.connected = False
        ECOM.eventManager.addListener(self.ipValidate, Event_IPInput.eventType)
    
    def init(self):
        self.client = Client()
    
    def update(self):
        if self.connected:
            inData = self.receive(False)
            if inData:
                if inData == "disconnect":
                    self.cleanUp()
                    return
                
                for event in inData:
                    ECOM.eventManager.queueEvent(event)
                
            if self.outData:
                self.client.send(self.outData)
                self.outData.clear()
            else:
                self.client.send("update")

    def connect(self):
        try:
            self.client.connect(self.ip, self.port)        
            self.connected = True
            return True
        except MM.MastermindErrorSocket:
            return False
            
    def send(self, data):
        self.outData.append(data)
    
    def receive(self, blocking = False):
        data = self.client.receive(blocking)
        return data
        
    def ipValidate(self, event):
        try:
            ipaddress.ip_address(event.ip)
        except ValueError:
            return
        
        self.ip = event.ip
        
        event = Event_IPValid(True) 
        ECOM.eventManager.queueEvent(event)
    
    def cleanUp(self):
        if self.connected:
            self.client.disconnect()
            self.client = None
        
        ECOM.eventManager.removeListener(self.ipValidate, Event_IPInput.eventType)


class NetworkEventForwarder:
    '''Used to send events across the network'''
    def __init__(self, networkManager):
        self.networkManager = networkManager
    
    def forwardEvent(self, event):
        self.networkManager.send(event)
        
        
        
        
        