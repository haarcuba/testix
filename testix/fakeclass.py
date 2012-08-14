from testix import fakeobject
import sys

class _FakeInit( fakeobject.FakeObject ):
	def __call__( self, * args, ** kwargs ):
		withoutSelf = args[ 1: ]
		fakeobject.FakeObject.__call__( self, * withoutSelf, ** kwargs )

def _fakeClassFactory( path ):
	_FakeClass = type( path, (), {} )
	_FakeClass.__init__ = _FakeInit( path )
	return _FakeClass	

def fakeClass( module, className ):
	newClass = _fakeClassFactory( '%s.%s' % ( module, className ) )
	setattr( sys.modules[ module ], className, newClass )
