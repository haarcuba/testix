
def send_some_data(socket, data):
    length = len(data)
    header = b'SIZE:' + bytes(str(length), encoding='latin-1')
    socket.send(header)
    socket.send(data)
