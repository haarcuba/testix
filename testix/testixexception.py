class TestixException( BaseException ):
	def __init__( self, message = '' ):
		self.message = message
		BaseException.__init__( self )

	def __str__( self ):
		return self.message

	def __rper__( self ):
		return str( self )

class ExpectationException( TestixException ):
	pass
