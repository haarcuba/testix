from testix import *

import server

def test_person_connects_somehow():
    with Scenario() as s:
        s.database.connect(IgnoreCallDetails())
        s.database.connect(IgnoreCallDetails())
        s.database.connect(IgnoreCallDetails())

        tested = server.Server(Fake('database'))
        tested.connect1()
        tested.connect2()
        tested.connect3()
