function! NewFile()
python << endpython
import os
import vim
from vim import *
extension = current.buffer.name.split( '.' )[ -1 ]
print extension
if extension == 'h':
	basename = os.path.basename( current.buffer.name )
	className = basename.split( '.' )[ 0 ]
	directory = os.path.dirname( current.buffer.name )
	relativeDirectory = os.path.relpath( directory, os.getcwd() )
	namespaces = relativeDirectory.split( '/' )[ 1: ]
	macro = '%s_%s' % ( '_'.join( namespaces ).upper(), basename.replace( '.', '_' ).upper() )
	current.buffer[ 0 ] = '#ifndef %s' % macro
	current.buffer.append( '#define %s' % macro )
	current.buffer.append( '' )
	for namespace in namespaces:
		current.buffer.append( 'namespace %s' % namespace )
		current.buffer.append( '{' )
	current.buffer.append( '' )
	current.buffer.append( 'class %s {' % className )
	current.buffer.append( '' )
	current.buffer.append( '};' )
	current.buffer.append( '' )
	for namespace in reversed( namespaces ):
		current.buffer.append( '} // %s' % namespace )
	current.buffer.append( '#endif // %s' % macro )
endpython
endfunction
map <F3> :call NewFile() <CR>
