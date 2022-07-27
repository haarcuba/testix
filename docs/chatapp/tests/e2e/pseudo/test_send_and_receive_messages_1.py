import chatapp.client


def test_send_and_receive_messages():
    alice_messages = []
    bob_messages = []
    alice = chatapp.client.Client('Alice', on_message=alice_messages.append)
    bob = chatapp.client.Client('Bob', on_message=bob_messages.append)

    alice.send('hi Bob', to='Bob')
    bob.send('hi Alice', to='Alice')

    assert alice_messages == ['hi Alice']
    assert bob_messages == ['hi Bob']


