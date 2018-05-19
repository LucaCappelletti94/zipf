from ...factories import ZipfFromText


class ZipfFromFile(ZipfFromText):
    def __init__(self, options=None):
        super().__init__(options)
        self._file_interface = lambda f: f.read()

    def set_interface(self, file_interface):
        """Sets the interface with which read the text content of the file"""
        self._file_interface = file_interface

    def run(self, path):
        """Loads and extracts a zipf from the given file"""
        with open(path, "r") as f:
            text = self._file_interface(f)
        return super().run(text)
