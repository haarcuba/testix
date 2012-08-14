import socket

class FakeModuleUser( object ):
	def createSocket( self ):
		self._socket = socket.socket()

	def socket( self ):
		return self._socket
