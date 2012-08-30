function! AllignParameters()
python << endpython
#plugin to align long parameter lists. Use when standing on the function call
import re
import vim
from vim import *
paramPattern = re.compile( '\( (.*) \)' )
afterParamPattern = re.compile( '(\).*)' )

line = vim.current.line
parameters = paramPattern.search( line ).groups()[ 0 ].strip().split( ', ' )
afterParameters = afterParamPattern.search( line ).groups()[ 0 ]
TAB = 4

lineWidth = line.count( '\t' ) * ( TAB - 1 ) + line.find( '(' ) + TAB
tabs = lineWidth / TAB
firstLine = line[ : line.find( '(' ) + 1 ] + '\t' + parameters[ 0 ] + ','
lines = [ firstLine ]
for i in xrange( 1, len( parameters ) - 1 ):
	lines.append( '\t' * tabs + parameters[ i ] + ',' )
lines.append( '\t' * tabs + parameters[ -1 ] + ' ' + afterParameters )

vim.current.range[ : ] = lines
endpython
endfunction
map <F6> :call AllignParameters() <CR>
