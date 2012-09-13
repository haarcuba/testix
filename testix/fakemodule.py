import sys
from testix import fakeobject

_fakeModules = {}

def _fakeSingleModule( name ):
	if name in _fakeModules:
		return
	_fakeModules[ name ] = fakeobject.FakeObject( name )
	sys.modules[ name ] = _fakeModules[ name ]
	components = name.split( '.' )
	if len( components ) > 1:
		parent = '.'.join( components[ :-1 ] )
		child = components[ -1 ]
		setattr( sys.modules[ parent ], child, _fakeModules[ name ] )

def fakeModule( name ):
	_fakeSingleModule( name )
