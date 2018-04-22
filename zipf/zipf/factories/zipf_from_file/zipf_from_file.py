from ...factories import zipf_from_text

class zipf_from_file(zipf_from_text):
    def __init__(self):
        super().__init__()
        self._file_interface = lambda f: f.read()

    def set_interface(self, file_interface):
        """Sets the interface with which read the text content of the file"""
        self._file_interface = file_interface

    def _load_file(self, path):
        with open(path, "r") as f:
            return self._file_interface(f)

    def run(self, path):
        """Loads and extracts a zipf from the given file"""
        return super().run(self._load_file(path))

    def enrich(self, path, _zipf):
        """Loads and enriches a given zipf from the given file"""
        return super().enrich(self._load_file(path), _zipf)