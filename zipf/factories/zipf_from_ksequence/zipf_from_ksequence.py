"""ZipfFromKSequence create a Zipf from a given sequence."""
from ...factories import ZipfFromList


class ZipfFromKSequence(ZipfFromList):
    """ZipfFromKSequence create a Zipf from a given sequence."""

    def __init__(self, k, options=None):
        """Create a ZipfFromKSequence with give options and k length."""
        super().__init__(options)
        if k <= 0:
            raise ValueError("The attribute k cannot be less than zero!")
        self.k = k

    def _split_sequences(self, sequence):
        """Return generator of subsequences of length k from given sequence."""
        n = len(sequence)
        return (sequence[i:i + self.k] for i in range(0, n, self.k))

    def run(self, sequence):
        """Return Zipf created from given sequence."""
        return super().run(self._split_sequences(sequence))
