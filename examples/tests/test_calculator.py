import unittest
from testix.frequentlyused import *

fakeModule( 'multiplier' )
from examples import calculator

class Test_Calculator( unittest.TestCase ):
	def construct( self, value ):
		self.tested = calculator.Calculator( value )

	def test_Addition( self ):
		self.construct( 5 )
		self.tested.add( 7 )
		self.assertEqual( self.tested.result(), 12 )
		self.tested.add( 1.5 )
		self.assertEqual( self.tested.result(), 13.5 )

	def test_MultiplicationUsesMultiplier( self ):
		self.construct( 5 )
		scenario = Scenario() <<\
			Call( 'multiplier.multiply', [], 35, kwargExpectations = { 'first': 5, 'second': 7 } ) <<\
			Call( 'multiplier.multiply', [], 350, kwargExpectations = { 'first': 35, 'second': 10 } )
		self.tested.multiply( 7 )
		self.assertEqual( self.tested.result(), 35 )
		self.tested.multiply( 10 )
		self.assertEqual( self.tested.result(), 350 )
		scenario.end()
