function NewFunction( name )
	let bufferName = bufname( "%" )
	echo name
endfunction

command -nargs=1  NewFunction  :call NewFunction(<q-args>)
