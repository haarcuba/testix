# TESTIX

Testix is a Mocking framework for Python, meant to be used with [pytest](https://docs.pytest.org/en/latest/).

[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)
[![GitHub release](version.svg)](https://GitHub.com/haarcuba/testix/releases/)


Testix is special because it allows you to specify what your mock objects do,
and it then enforces your specifications automatically. It also reduces (albeit
not entirely) mock setup. Other frameworks usually have a flow like this:

* setup mock
* let code do something with mock
* assert mock used in correct way

Testix flow is a bit different
* setup mock objects (`sock` in the following example)
* specify exactly what should happen to them using a Scenario context


# TOC

* [Documentation](#documentation)
* [Small Example](#small-example)
* [Installation](#installation)
* [Python 3 and Legacy Python](#legacy)
* [Advanced Features](#advanced-features)


## Documentation <a name="documentation></a>

Read the full docs at [readthedocs](https://testix.readthedocs.io/en/latest/)

## Small Example <a name="small-example"></a>
Here's a small example:

```python
    # create your object under test, pass in some mock objects
    # in production, Chatbot will receive and actual socket object
    # here we want to test what it does with the socket it receives
    # and we do not want it to actually communicate with anyone
    # to both those ends, we pass a mock, or fake, object.
    self.tested = chatbot.Chatbot(Fake('sock')) # Fake('sock') is a mock object named "sock"

    # create a Scenario context
    # inside, you specify exactly what the unit should do with the objects its handed
    with Scenario() as s:

        # we can refer here to s.sock, because there is a mock named `sock`
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
it. Only "top level" mock objects need to be setup explicitly.

Continue reading for further examples.


## Installation <a name="installation"></a>
With `pip`:

    $ pip install testix

## Python 3 and Legacy Python (Python 2) <a name="legacy"></a>

Testix works with Python 3. It will not work with legacy python.


### Credit Where it's due
Testix started as a re-implementation of ideas from the [Voodoo-Mock](http://sourceforge.net/projects/voodoo-mock)
unit-testing framework. Since then it has evolved some different traits though.

### License

This software is available under the MIT License, see the `LICENSE` file.
