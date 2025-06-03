import traceback


def format(name, args, kwargs):
    if 'async_iterator_a62df12dd67848be82c505d63b928725' in name:
        root, _ = name.split('.')
        return '(async for on {root})'.format(root=root)
    if len(args) > 0:
        argsString = ', '.join([repr(arg) for arg in args])
    else:
        argsString = None
    if len(kwargs) > 0:
        kwargsString = ', '.join('{key} = {value}'.format(key=key, value=repr(value)) for (key, value) in kwargs.items())
    else:
        kwargsString = None

    if (argsString, kwargsString) == (None, None):
        return '{}()'.format(name)

    if argsString is not None and kwargsString is None:
        return '{name}({argsString})'.format(name=name, argsString=argsString)

    if argsString is None and kwargsString is not None:
        return '{name}({kwargsString})'.format(name=name, kwargsString=kwargsString)

    return '{name}({argsString}, {kwargsString})'.format(name=name, argsString=argsString, kwargsString=kwargsString)


def caller_context():
    stack = traceback.extract_stack()
    for index, frame_summary in enumerate(stack):
        if 'return self.__returnResultFromScenario' in frame_summary.line:
            break

    frame_summary = stack[index - 1]
    return '{line} ({filename}:{lineno})'.format(line=frame_summary.line, filename=frame_summary.filename, lineno=frame_summary.lineno)
