def format( name, args, kwargs ):
    if len( args ) > 0:
        argsString = ', '.join( [ str( arg ) for arg in args ] )
    else:
        argsString = None
    if len( kwargs ) > 0:
        kwargsString = ', '.join( f'{key} = {value}' for (key, value) in kwargs.items() )
    else:
        kwargsString = None

    if (argsString, kwargsString) == (None, None):
        return f'{name}()'

    if argsString is not None and kwargsString is None:
        return f'{name}({argsString})'

    if argsString is None and kwargsString is not None:
        return f'{name}({kwargsString})'

    return f'{name}({argsString}, {kwargsString})'

