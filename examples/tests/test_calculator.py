from testix.asserts import *
from testix import suite

from examples import calculator

class Test_Calculator( suite.Suite ):
	def construct( self, value ):
		self.tested = calculator.Calculator( value )

	def test_Addition( self ):
		self.construct( 5 )
		self.tested.add( 7 )
		TS_ASSERT_EQUALS( self.tested.result(), 12 )
		self.tested.add( 1.5 )
		TS_ASSERT_EQUALS( self.tested.result(), 13.5 )
