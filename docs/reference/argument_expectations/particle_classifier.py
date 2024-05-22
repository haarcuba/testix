class ParticleClassifier:
    def __init__(self, spin_verifier):
        self._spin_verifier = spin_verifier

    def classify(self, mass, spin):
        self._spin_verifier(spin)
        # other logic here
