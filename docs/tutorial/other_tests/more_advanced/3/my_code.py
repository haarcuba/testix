def go(source, destination):
    names = source.get_names('all', order='lexicographic', ascending=True)
    destination.put_names(names)
