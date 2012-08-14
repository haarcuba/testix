from testix import scenario
from testix import exception

_registry = {}
class _MagicExposePath( object ): pass

class FakeObject( object ):
	def __init__( self, path ):
		self._path = path
		_registry[ path ] = self

	def __call__( self, * args, ** kwargs ):
		if len( args ) == 1:
			if args[ 0 ] is _MagicExposePath:
				return self._path
		return self._returnResultFromScenario( * args, ** kwargs )

	def _returnResultFromScenario( self, * args, ** kwargs ):
		if scenario.current() is None:
			raise exception.Exception( "can not find a scenario object" )
		return scenario.current().resultFor( self._path, * args, ** kwargs )

	def __str__( self ):
		return 'FakeObject( "%s", %s )' % ( self._path, id( self ) )

	def __repr__( self ):
		return str( self )

	def __getattr__( self, name ):
		childsName = '%s.%s' % ( self._path, name )
		if childsName in _registry:
			return _registry[ childsName ]
		else:
			return FakeObject( childsName )

def exposePath( fakeObject ):
	return fakeObject( _MagicExposePath )
