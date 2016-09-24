class StarterTestCollection( object ):
	def __init__( self ):
		self._run()

	def _run( self ):
		testsRun = 0
		for key in sorted( self.__class__.__dict__.keys() ):
			if key.startswith( 'starter_test' ):
				self.setup()
				test = getattr( self, key )
				test()
				testsRun += 1
				self.tearDown()
		print( '%d tests' % testsRun )

	def tearDown( self ):
		pass

	def setup( self ):
		pass
