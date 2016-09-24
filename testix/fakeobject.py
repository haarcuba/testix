from testix import scenario
from testix import testixexception
import sys

class FakeObject( object ):
        _registry = {}

        def __new__( cls, path ):
                if path in FakeObject._registry:
                        return FakeObject._registry[ path ]
                instance = super( FakeObject, cls ).__new__( cls )
                FakeObject._registry[ path ] = instance
                return instance

        @classmethod
        def clearNonModuleFakeObjects( cls ):
                keys = list( FakeObject._registry.keys() )
                for path in keys:
                        if path in sys.modules:
                                continue
                        del FakeObject._registry[ path ]

        def __init__( self, path ):
                self._path = path

        def __call__( self, * args, ** kwargs ):
                return self._returnResultFromScenario( * args, ** kwargs )

        def _returnResultFromScenario( self, * args, ** kwargs ):
                if scenario.current() is None:
                        raise testixexception.TestixException( "can not find a scenario object" )
                return scenario.current().resultFor( self._path, * args, ** kwargs )

        def __str__( self ):
                return 'FakeObject( "%s", %s )' % ( self._path, id( self ) )

        def __repr__( self ):
                return str( self )

        def __getattr__( self, name ):
                childsName = '%s.%s' % ( self._path, name )
                return FakeObject( childsName )

def clearNonModuleFakeObjects():
        FakeObject.clearNonModuleFakeObjects()
