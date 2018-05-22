"""ZipfFromUrl create a Zipf from an the document at a given url."""
import requests

from ...factories import ZipfFromText


class ZipfFromUrl(ZipfFromText):
    """ZipfFromUrl create a Zipf from an the document at a given url."""

    def __init__(self, options=None):
        """Create a ZipfFromUrl with give options."""
        super().__init__(options)
        self._request_interface = lambda r: r.text

    def set_interface(self, request_interface):
        """Set the interface with which read the text content of the file."""
        self._request_interface = request_interface

    def _download_file(self, url):
        """Return the document from given url."""
        r = requests.get(url)
        return self._request_interface(r)

    def run(self, url):
        """Load and extract zipf from the given url."""
        return super().run(self._download_file(url))
