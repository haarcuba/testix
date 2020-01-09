from testix import scenario
from testix import failhooks

class Fake:
    _registry = {}
    def __new__( cls, path, **attributes ):
        if path in Fake._registry:
            return Fake._registry[path]
        instance = super(Fake, cls).__new__(cls)
        Fake._registry[path] = instance
        return instance

    @staticmethod
    def clear_all_attributes():
        for instance in Fake._registry.values():
            Fake.clear_attributes(instance)

    @staticmethod
    def clear_attributes(instance):
        variables = list(vars(instance).keys())
        for key in variables:
            if key.startswith('_'):
                continue
            delattr(instance, key)

    scenario.Scenario.init_hook = clear_all_attributes

    def __init__( self, path, **attributes ):
        self._path = path
        self._set_attributes(attributes)

    def _set_attributes(self, attributes):
        for key, value in attributes.items():
            setattr(self, key, value)

    def __call__( self, * args, ** kwargs ):
        return self._returnResultFromScenario( * args, ** kwargs )

    def _returnResultFromScenario( self, * args, ** kwargs ):
        if scenario.current() is None:
            failhooks.error( "can not find a scenario object" )
        return scenario.current().resultFor( self._path, * args, ** kwargs )

    def __str__( self ):
        return 'FakeObject( "%s", %s )' % ( self._path, id( self ) )

    def __repr__( self ):
        return str( self )

    def __getattr__( self, name ):
        childsName = '%s.%s' % ( self._path, name )
        return Fake(childsName)
