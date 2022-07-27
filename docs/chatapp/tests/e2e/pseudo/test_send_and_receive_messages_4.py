import pytest
import chatapp.client
import chatapp.server
import time

class OnMessage:
    def __init__(self):
        self.messages = []

    def __call__(self, client, message, peer):
        self.messages.append({'message': message, 'peer': peer})

@pytest.fixture
def chat_app_server():
    server = chatapp.server.Server(bind_to=('', 3333))
    server.start()
    yield 'http://localhost:3333'
    server.stop()

def test_send_and_receive_messages(chat_app_server):
    alice_callback = OnMessage()
    bob_callback = OnMessage()
    alice = chatapp.client.Client('Alice', on_message=alice_callback, server_url=chat_app_server)
    bob = chatapp.client.Client('Bob', on_message=bob_callback, server_url=chat_app_server)

    alice.send('hi Bob', to='Bob')
    bob.send('hi Alice', to='Alice')

    LET_SERVER_RELAY_MESSAGES = 3
    time.sleep(LET_SERVER_RELAY_MESSAGES)

    assert alice_callback.messages == [{'message': 'hi Alice', 'peer': 'Bob'}]
    assert bob_callback.messages   == [{'message': 'hi Bob',   'peer': 'Alice'}]
