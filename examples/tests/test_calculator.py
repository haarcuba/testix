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
        with Scenario() as scenario:
            scenario <<\
                Call( 'multiplier.multiply', first = 5, second = 7 ).returns( 35 ) <<\
                Call( 'multiplier.multiply', first = 35, second = 10 ).returns( 350 )
            self.tested.multiply( 7 )
            self.assertEqual( self.tested.result(), 35 )
            self.tested.multiply( 10 )
            self.assertEqual( self.tested.result(), 350 )
