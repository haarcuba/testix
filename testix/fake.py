from testix import scenario
from testix import failhooks


class Fake:
    __registry = {}
    __fake_module = set()

    def __new__(cls, path_a62df12dd67848be82c505d63b928725, **attributes):
        if path_a62df12dd67848be82c505d63b928725 in Fake.__registry:
            return Fake.__registry[path_a62df12dd67848be82c505d63b928725]
        instance = super(Fake, cls).__new__(cls)
        Fake.__registry[path_a62df12dd67848be82c505d63b928725] = instance
        return instance

    @staticmethod
    def exempt_from_attribute_sweep(path_a62df12dd67848be82c505d63b928725):
        Fake.__fake_module.add(path_a62df12dd67848be82c505d63b928725)

    @staticmethod
    def unexempt_from_attribute_sweep(path_a62df12dd67848be82c505d63b928725):
        if path_a62df12dd67848be82c505d63b928725 not in Fake.__fake_module:
            return
        Fake.__fake_module.remove(path_a62df12dd67848be82c505d63b928725)

    @staticmethod
    def clear_all_attributes():
        for instance in Fake.__registry.values():
            if instance.path_a62df12dd67848be82c505d63b928725 in Fake.__fake_module:
                continue
            Fake.clear_attributes(instance)

    @staticmethod
    def clear_attributes(instance):
        variables = list(vars(instance).keys())
        for key in variables:
            if key.startswith('_'):
                continue
            delattr(instance, key)

    scenario.Scenario.init_hook = clear_all_attributes

    def __init__(self, path_a62df12dd67848be82c505d63b928725, **attributes):
        self.__path = path_a62df12dd67848be82c505d63b928725
        self.__set_attributes(attributes)

    def __setitem__(self, key, value):
        self.__setitem__a62df12dd67848be82c505d63b928725 = Fake('{root}.__setitem__'.format(root=self.__path))
        self.__setitem__a62df12dd67848be82c505d63b928725(key, value)

    @property
    def path_a62df12dd67848be82c505d63b928725(self):
        return self.__path

    def __set_attributes(self, attributes):
        for key, value in attributes.items():
            setattr(self, key, value)

    def __call__(self, *args, **kwargs):
        return self.__returnResultFromScenario(*args, **kwargs)

    def __returnResultFromScenario(self, *args, **kwargs):
        if scenario.current() is None:
            failhooks.error("can not find a scenario object")
        return scenario.current().resultFor(self.__path, *args, **kwargs)

    def __str__(self):
        return 'FakeObject( "%s", %s )' % (self.__path, id(self))

    def __repr__(self):
        return str(self)

    def __getattr__(self, name):
        childsName = '%s.%s' % (self.__path, name)
        return Fake(childsName)

    def __aiter__(self):
        async_iterator_fake = self.async_iterator_a62df12dd67848be82c505d63b928725

        async def fakeIterator():
            iterable = async_iterator_fake()
            for item in iterable:
                yield item

        return aiter(fakeIterator())
