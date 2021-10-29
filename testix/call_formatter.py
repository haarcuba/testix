import traceback

def format( name, args, kwargs ):
    if len( args ) > 0:
        argsString = ', '.join( [ repr( arg ) for arg in args ] )
    else:
        argsString = None
    if len( kwargs ) > 0:
        kwargsString = ', '.join( f'{key} = {repr(value)}' for (key, value) in kwargs.items() )
    else:
        kwargsString = None

    if (argsString, kwargsString) == (None, None):
        return f'{name}()'

    if argsString is not None and kwargsString is None:
        return f'{name}({argsString})'

    if argsString is None and kwargsString is not None:
        return f'{name}({kwargsString})'

    return f'{name}({argsString}, {kwargsString})'

def caller_context():
    stack = traceback.extract_stack()
    for index, frame_summary in enumerate(stack):
        if 'return self.__returnResultFromScenario' in frame_summary.line:
            break

    frame_summary = stack[index-1]
    return f'{frame_summary.line} ({frame_summary.filename}:{frame_summary.lineno})'
