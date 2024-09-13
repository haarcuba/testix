def send_some_data(socket, data):
    length = len(data)
    header = b'SIZE:' + bytes(str(length), encoding='latin-1') + b' '
    socket.send(header)
    socket.send(data)
