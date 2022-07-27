.. include:: ../common.rst

Design of the Chat App
======================

We'll have an HTTP based server, and 
a small client library that sends and receives messages 
from said server.

So we have

* HTTP Based Chat Server relaying messages between clients
* Client library that sends and receives messages to/from other clients via the Chat Server

Since this is a Test Driven Development tutorial as well as a |testix| tutorial,
let's discuss the tests.

We will have both *unit tests* and *integration tests*.

Unit Tests
----------

Unit tests check that each unit of code (usually a single class or module) performs the correct business logic.

Generally speaking, unit tests

* test logic
* do not perform I/O (perhaps only to local files)
* use mocks (not always, but many times)

Integration Tests
-----------------

Integration tests test that various "units" fit together.

Generally speaking, integration tests

* perform some actual I/O
* do not rigorously test logic (that's the unit test's job)


End-to-End (E2E) Tests
----------------------

In our case, since the app is quite simple,
the integration test will actually test the entire app,
and so it is more appropriately called an End-to-End (E2E) Test.

In real projects, E2E tests usually include also an actual deployment,
which is as similar as possible to real life deployments.

In our toy example, we don't have such complications.

Let's move on.
