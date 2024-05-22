from testix import *
import pytest

import particle_classifier

def my_exception_factory():
    return Exception('bad spin value')

def test_allow_spin_verifier_to_raise_exceptions():
    with Scenario() as s:
        s.spin_verifier('some spin value') >> Throwing(my_exception_factory)
        tested = particle_classifier.ParticleClassifier(Fake('spin_verifier'))
        with pytest.raises(Exception, match='bad spin value'):
            tested.classify(mass='0.5MeV', spin='some spin value')
