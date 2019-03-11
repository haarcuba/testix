# TESTIX

Testix is a Mocking framework for Python, meant to be used with [pytest](https://docs.pytest.org/en/latest/).


Testix is special because it allows you to specify what your mock objects do,
and it then enforces your specifications automatically. It also reduces (albeit
not entirely) mock setup. Other frameworks usually have a flow like this:

* setup mock
* let code do something with mock
* assert mock used in correct way

Testix flow is a bit different
* setup "top level" mock objects (`sock` in the following example)
* specify exactly what should happen to them using a scenario

And that's it.  Here's a small example:

```python
    # create your object under test, pass in some mock objects
    self.tested = chatbot.Chatbot( FakeObject( 'sock' ) )

    # create a Scenario context
    # inside, you specify exactly what the unit should do with the objects its handed
    with Scenario() as s:


        s.sock.recv(4096) >> 'request text'  # unit must call sock.recv(4096).
                                             # this call will return 'request text'
        s.sock.send('response text')

        # call your unit's code
        self.tested.go()


# Scenario context ends, and verifies everything happened exactly as specified
# No more, no less
```

Note that you do not have to setup `sock.recv` or `sock.send` - once `sock` is
set up, it will generate other mock objects automatically as you go along with
it. That's what was meant by "top level" mocks earlier.


## Installation
With `pip`:

    $ pip install testix

## Python 3 and Legacy Python (Python 2)

Testix works with Python 3. It will not work in legacy python.

# Extended Example

In this example we will test a `Chatbot` object.
The `Chatbot` receives a socket through its `__init__` function.
It also delegates the actual data from the socket to a responder object,
which it will build by instantiating a `Responder` object from the `Responder` class
inside the `responder` module, which the `chatbot` module imports.

The skeleton `chatbot` module looks like this:
```python
import socket
from . import responder 

class Chatbot:
    def __init__( self, peer ): # peer is the socket connected to the other side
        pass
```

## Construction Test

Now let's see the unit tests. Our first demand is that a `Chatbot` object generates a `Responder` object as it's constructed:

```python
import pytest
import socket
from testix.frequentlyused import *  # import testix DSL objects e.g. Scenario, FakeObject
from testix import patch_module      # a fixture used for patching names at the module level
from chatbot import chatbot          # the module under test

class TestChatbot:
    @pytest.fixture(autouse=True) # autouse will make this fixture run for every test function
    def globals_patch(self, patch_module):
        patch_module( chatbot, 'responder' )    # replace chatbot.responder with a mock which we can trace using a Scenario

    def test_construction(self):
        with Scenario() as s:
            # this is our demand: before this Scenario context is finished,
            # the code *must* call responder.Responder(). This call will return
            # a mock (the FakeObject) labled 'responder_'
            # 
            # I'm using 'responder_' so as not to refer to the mock replacing the responder module,
            # which I set up in the globals_patch fixture
            s.responder.Responder() >> FakeObject( 'responder_' )

            # now call the code, pass in a mock object instead of a socket
            # we'll use this mock later
            self.tested = chatbot.Chatbot( FakeObject( 'sock' ) )
```

Running `pytest` with this test will result in the following failure (since we did not yet write the code)

        def _fail_py_test( exceptionFactory, message ):
    >       return pytest.fail( message )
    E       Failed:
    E       testix: ScenarioException
    E       testix details:
    E       Scenario ended, but not all expectations were met. Pending expectations (ordered):
    [responder.Responder()]

As you can see, Testix complains that it expected the `responder.Responder()`
call, but it did not happen.

Let's write the code that passes this test:

```python
# chatbot.py
import socket
from . import responder 

class Chatbot:
    def __init__( self, peer ):
        self._responder = responder.Responder()
```

This will pass the test. Before we continue, let's refactor so that we can reuse the object construction in further tests:

```python
class TestChatbot:
    @pytest.fixture(autouse=True)
    def globals_patch(self, patch_module):
        patch_module( chatbot, 'responder' )

    def construct(self):
        with Scenario() as s:
            s.responder.Responder() >> FakeObject( 'responder_' )
            self.tested = chatbot.Chatbot( FakeObject( 'sock' ) )

    def test_construction(self):
        self.construct()
```

## Testing the Endless Request-Response Loop

We want to add a `.go()` method to the `Chatbot`. This method will run an
endless loop that reads from the socket, gets a response from the responder,
and writes it back to the socket. First, let's write a skeleton `go` function:

```python
class Chatbot:
    def __init__( self, peer ):
        self._peer = peer
        self._responder = responder.Responder()

    def go(self):
        pass
```

Now, here's the test:

```python
class TestChatbot:
    ...
    def test_request_response_loop(self):
        self.construct()

        with Scenario() as s:
            # let's do a 10-time loop
            # this for loop makes 30 (10 times 3) *demands* of our chatbot
            for i in range(10):
                # call .recv(4096) on the socket
                # we set it up to return the string f'request {i}'
                s.sock.recv(4096)                     >> f'request {i}'

                # call .process(f'request {i}') on the responder object
                # which will return the response in real life - here
                # we make it return a fake f'response {i}' string
                s.responder_.process(f'request {i}')  >> f'response {i}'

                # call .send on the socket with the response we got
                s.sock.send(f'response {i}')

            # now actually do the work
            self.tested.go()
```

Of course, you should run this test and see it fail with 30 pending expectations.
Let's write our code:

```python
class Chatbot:
    ...
    def go(self):
        while True:
            request = self._peer.recv(4096)
            response = self._responder.process(request)
            self._peer.send(response)
```

Running this code produces another failure:

        def _fail_py_test( exceptionFactory, message ):
    >       return pytest.fail( message )
    E       Failed:
    E       testix: ExpectationException
    E       testix details:
    E       unexpected call: sock.recv(4096)
    E       Expected nothing

What happened? Well, while our code does what we want, our test does not actually express what we meant. The test specifies exactly 10 rounds of the loop, so once those are over, and the infinite while loop runs for the 11th time, the `.recv(4096)` is called, and this is not specified in our `Scenario`, so Testix fails the test.

Remember, Testix verifies your scenario *exactly*, no more, no less. We've seen the "no less" side of things, no we see the "no more" side.

So, how do you test an infinite loop without getting stuck? For this, I use a trick, which also introduces another Testix feature, the `.throwing` expectation. You see, we can not only make mock function calls return what we want, we can make them raise exceptions. Here's the correct test:

```python
class EndTestException(Exception): pass # dummy exception to end the test

class TestChatbot:
    ...
    def test_request_response_loop(self):
        self.construct()
        with Scenario() as s:
            for i in range(10):
                s.sock.recv(4096)                       >> f'request {i}'
                s.responder_.process(f'request {i}')    >> f'response {i}'
                s.sock.send(f'response {i}')

            # specify that the next recv call throws an EndTestException object
            s.sock.recv(4096).throwing(EndTestException)

            # use pytest to verify that this exception is actually thrown
            with pytest.raises(EndTestException):
                self.tested.go()
```

## Testing Resilience to Exceptions

Let's add one more test - we demand that our infinite loop not crash in case the `recv` call raises and error. Here's the test:

```python
class TestChatbot:
    ...
    def test_request_response_loop_survives_a_recv_exception(self):
        self.construct()
        class EndTestException(Exception): pass
        with Scenario() as s:
            # first 10 times go smoothly
            for i in range(10):
                s.sock.recv(4096)                       >> f'request {i}'
                s.responder_.process(f'request {i}')    >> f'response {i}'
                s.sock.send(f'response {i}')

            # uh-oh, the socket raises an error!
            s.sock.recv(4096).throwing(socket.error)

            # we are resilient! we continue the loop
            for i in range(10):
                s.sock.recv(4096)                       >> f'request {i}'
                s.responder_.process(f'request {i}')    >> f'response {i}'
                s.sock.send(f'response {i}')

            # end the infinite loop by throwing an exception that
            # the code does not catch, as before
            s.sock.recv(4096).throwing(EndTestException)
            with pytest.raises(EndTestException):
                self.tested.go()
```

Running this test now will result in this failure:

    self = sock.recv(4096)

        def result( self ):
            if self._throwing:
    >           raise self._exceptionFactory()
    E           OSError

Well, turns out the `socket.error` and `OSError` are one and the same. I didn't
know that before. At any rate, this is thrown from `recv` and kills the test.

Let's continue and write the code that handles this:

```python
class Chatbot:
    ...
    def go(self):
        while True:
            try:
                request = self._peer.recv(4096)
                response = self._responder.process(request)
                self._peer.send(response)
            except socket.error:
                pass
```

## Readability Options

You may specify a return value for a mock in two ways:

1. Using `>>`
    ```python
        s.sock.send('some text') >> return_value
    ```
2. Using `.returns`
    ```python
        s.sock.send('some text').returns( return_value )
    ```

## Advantages over `unittest.mock`

Compare this `unittest.mock` based version of `test_request_response_loop` from above:
```python
    @patch('chatbot.responder.Responder')
    def test_request_response_loop(self, Responder):
        sock = Mock()
        responder = Mock()
        Responder.side_effect = [ responder ]
        self.construct(sock, Responder)
        class EndTestException(Exception): pass

        REQUESTS = [f'request {i}' for i in range(10)]
        RESPONSES = [f'response {i}' for i in range(10)]
        responder.process.side_effect = RESPONSES
        sock.recv.side_effect = REQUESTS + [EndTestException]
        
        with pytest.raises(EndTestException):
            self.tested.go()

        sock.recv.assert_has_calls( [ call(4096) ] * 10 )
        responder.process.assert_has_calls( [ call(request) for request in requests ] )
        sock.send.assert_has_calls( [ call( response ) for response in RESPONSES ] )
```

In my opinion, at least, the `testix` based version was better.

* With Testix, Defining how the mocks are called and asserting that they actually were called that way is one and the same. Using `unittest.mock` these are two separate stages, one may easily forget to make some assertions.
* Testix scenario specification is much more readable

# Advanced Features

There are a few, but for now this is a TODO section.

# More Info

### Credit Where it's due
Testix started as a re-implementation of ideas from the [Voodoo-Mock](http://sourceforge.net/projects/voodoo-mock)
unit-testing framework. Since then it has evolved some different traits though.

### License
This software is free software, and is distributed under the GNU General Public License version 3.0.
See the COPYING file for details.
