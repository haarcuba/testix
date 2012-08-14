from testix import suite
from testix.startertests.asserts import *
from testix.startertests import startertestcollection

class StarterTestSuite( startertestcollection.StarterTestCollection ):
	def starter_test_SuiteRunsOneTest( self ):
		class MySuite( suite.Suite ):
			def __init__( self ):
				self.wasRun = False
				suite.Suite.__init__( self )

			def test_FlagUp( self ):
				self.wasRun = True

		mySuite = MySuite()
		mySuite.run()
		STS_ASSERT( mySuite.wasRun )

	def starter_test_SuiteRunsMultipleTests( self ):
		class MultipleTestsSuite( suite.Suite ):
			def __init__( self ):
				self.wasRun = []
				suite.Suite.__init__( self )

			def test_First( self ):
				self.wasRun.append( 'First' )

			def test_Second( self ):
				self.wasRun.append( 'Second' )

			def test_Third( self ):
				self.wasRun.append( 'Third' )

		multipleTestSuite = MultipleTestsSuite()
		multipleTestSuite.run()
		STS_ASSERT_EQUALS( set( multipleTestSuite.wasRun ), set( [ 'First', 'Second', 'Third' ] ) )

	def starter_test_DontRunNonTestMethods( self ):
		class DontRunNonTestMethods( suite.Suite ):
			def __init__( self ):
				self.wasRun = False

			def notest_ThisShouldNotRun( self ):
				self.wasRun = True

		tested = DontRunNonTestMethods()
		tested.run()
		STS_ASSERT_EQUALS( tested.wasRun, False )

StarterTestSuite()
