from testix import fakeobject
import pprint

class ArgumentExpectation( object ):
	def __init__( self, value ):
		self.expectedValue = value

	def ok( self, value ):
		raise Exception( "must override this" )

	def __repr__( self ):
		return pprint.pformat( self.expectedValue )

class ArgumentEquals( ArgumentExpectation ):
	def ok( self, value ):
		return self.expectedValue == value

class ArgumentIsFakeObjectWithPath( ArgumentExpectation ):
	def ok( self, value ):
		if not isinstance( value, fakeobject.FakeObject ):
			return False
		expectedPath = self.expectedValue
		return value is fakeobject.FakeObject( expectedPath )

	def __repr__( self ):
		return "|%s|" % self.expectedValue

class IgnoreArgument( ArgumentExpectation ):
	def __init__( self ):
		ArgumentExpectation.__init__( self, 0 )

	def ok( self, value ):
		return True

	def __repr__( self ):
		return '|IGNORED|'

class ArgumentIs( ArgumentExpectation ):
	def ok( self, value ):
		return value is self.expectedValue

	def __repr__( self ):
		return '|IS %s|' % self.expectedValue
