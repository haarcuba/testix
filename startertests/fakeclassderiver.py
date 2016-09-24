import bogusmodule

class Derived( bogusmodule.BogusClass ):
	def __init__( self, arg1, arg2 ):
		bogusmodule.BogusClass.__init__( self, arg1, arg2 )
