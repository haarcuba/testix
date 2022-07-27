import chatapp.client
import time

class OnMessage:
    def __init__(self):
        self.messages = []

    def __call__(self, client, message, peer):
        self.messages.append({'message': message, 'peer': peer})

def test_send_and_receive_messages():
    alice_callback = OnMessage()
    bob_callback = OnMessage()
    alice = chatapp.client.Client('Alice', on_message=alice_callback)
    bob = chatapp.client.Client('Bob', on_message=bob_callback)

    alice.send('hi Bob', to='Bob')
    bob.send('hi Alice', to='Alice')

    LET_SERVER_RELAY_MESSAGES = 3
    time.sleep(LET_SERVER_RELAY_MESSAGES)

    assert alice_callback.messages == [{'message': 'hi Alice', 'peer': 'Bob'}]
    assert bob_callback.messages   == [{'message': 'hi Bob',   'peer': 'Alice'}]
