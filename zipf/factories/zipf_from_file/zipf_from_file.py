"""ZipfFromFile create a Zipf from an the document at a given path."""
from ...factories import ZipfFromText


class ZipfFromFile(ZipfFromText):
    """ZipfFromFile create a Zipf from an the document at a given path."""

    def __init__(self, options=None):
        """Create a ZipfFromFile with give options."""
        super().__init__(options)
        self._file_interface = lambda f: f.read()

    def set_interface(self, file_interface):
        """Set the interface with which read the text content of the file."""
        self._file_interface = file_interface

    def run(self, path):
        """Load and extract zipf from the given file."""
        with open(path, "r") as f:
            text = self._file_interface(f)
        return super().run(text)
