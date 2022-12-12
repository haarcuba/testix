from testix import Fake
from testix import Scenario
from testix.patch_module import Patcher

class AnObject:
    pass

def test_override_object_attribute_with_fake():
    patcher = Patcher()
    thing = AnObject()
    thing.name = 'original'
    patcher(thing, 'name')
    assert thing.name is Fake('name')
    patcher.undo()
    assert thing.name is 'original'

def test_override_object_attribute_with_arbitrary_object():
    patcher = Patcher()
    thing = AnObject()
    thing.name = 'original'
    patcher(thing, 'name', 'arbitrary object')
    assert thing.name is 'arbitrary object'
    patcher.undo()
    assert thing.name is 'original'

def test_override_non_existing_attribute():
    patcher = Patcher()
    thing = AnObject()
    assert not hasattr(thing, 'made_up_attribute')
    patcher(thing, 'made_up_attribute')
    assert thing.made_up_attribute is Fake('made_up_attribute')
    patcher.undo()
    assert not hasattr(thing, 'made_up_attribute')

def test_scenario_should_not_reset_fake_modules():
    patcher = Patcher()
    thing = AnObject()
    thing.name = 'original'
    patcher(thing, 'name')
    assert thing.name is Fake('name')
    thing.name.length = 111
    with Scenario() as s:
        assert thing.name.length == 111
    patcher.undo()
    assert thing.name is 'original'
