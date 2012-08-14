import sys
from testix import fakeobject

_fakeModules = {}

def _fakeSingleModule( name ):
	if name in _fakeModules:
		return
	components = name.split( '.' )
	_fakeModules[ name ] = fakeobject.FakeObject( name )
	sys.modules[ name ] = _fakeModules[ name ]
	if len( components ) > 1:
		parent = '.'.join( components[ :-1 ] )
		child = components[ -1 ]
		setattr( sys.modules[ parent ], child, _fakeModules[ name ] )

def fakeModule( name ):
	components = name.split( '.' )
	nameComponents = []
	while len( components ) > 0:
		nameComponents.append( components.pop( 0 ) )
		_fakeSingleModule( '.'.join( nameComponents ) )
