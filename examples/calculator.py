import multiplier

class Calculator( object ):
	def __init__( self, initialValue ):
		self._value = initialValue

	def add( self, addend ):
		self._value += addend

	def result( self ):
		return self._value

	def multiply( self, factor ):
		self._value = multiplier.multiply( first = self._value, second = factor )
