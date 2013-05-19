class Hook( object ):
	def __init__( self, callable, * args, ** kwargs ):
		self._callable = callable
		self._args = args
		self._kwargs = kwargs

	def execute( self ):
		self._callable( * self._args, ** self._kwargs )
