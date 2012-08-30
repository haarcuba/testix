function! CBlock()
python << endpython
import vim
from vim import *
def _normal( string ):
	vim.command( "normal %s" % string )
def firstWord( string ):
	words = string.split()
	if len( words ) > 0:
		return words[ 0 ]
	else:
		return ''
if firstWord( current.line ) in ( 'while', 'while(', 'for', 'for(', 'if', 'if(', 'do' ):
	_normal( "$a {" )
	_normal( "o}" )
else:
	_normal( "o{" )
	_normal( "o}" )
endpython
endfunction
imap <C-B> <ESC> k :call CBlock() <CR> kO
