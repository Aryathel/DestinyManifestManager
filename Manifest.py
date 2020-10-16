"""
.. module:: Manifest
    :platform: Unix, Windows
    :synopsis: The Destiny 2 API manifest manager.
"""

# Stdlib imports
import os
import zipfile

# 3rd Party Imports
import requests

# Local imports
from .Errors import LocaleException

# Some general constantsc
D2_API_BASE = "https://www.bungie.net/Platform"
D2_MANIFEST = D2_API_BASE + "/Destiny2/Manifest/"

class Manifest:
    """A manager built to function with the Destiny 2 Bungie API Manifests.

    The manager is used to download, update, and organize manifests for game data from Destiny 2.
    Bungie makes these available publicly through their api.

    .. note::
        This is an **in development** build, and will likely have many bugs.
    """
    def __init__(self, loc=None, headers=None):
        """A class made to manage data from te Destiny 2 API manifests.

        Kwargs:
            loc (str): The folder to store manifest data in.
            headers (headers): A dict of headers to attach to any requests.
        """
        self.manifestBase = D2_MANIFEST
        self.headers = headers
        self.loc = loc
        self.manifests = {
			'en': '',
			'fr': '',
			'es': '',
			'de': '',
			'it': '',
			'ja': '',
			'pt-br': '',
			'es-mx': '',
			'ru': '',
			'pl': '',
			'ko': '',
			'zh-cht': '',
			'zh-chs': ''
		}

    def update_manifest(self, language):
        """Updates the Destiny 2 manifest for a given locale.

        Retrieves the manifest for a selected locale and saves it locally. If the
        local file is not found, a new one will be created.

        **Parameters**:
            - **language** (:class:`str`) -
                A string representing the language locale.

        **Raises**:
            - :class:`LocaleException` -
                An error in accessing the  provided locale.
        """
        language = language.lower()
        if self.manifests.get(language, None) == None:
            raise LocaleException(f"The \'{language}\' locale could not be found.")

        manifestJson = requests.get(self.manifestBase, headers = self.headers).json()
        manifestUrl = 'https://www.bungie.net' + manifestJson['Response']['mobileWorldContentPaths'][language]
        manifestFileName = f"./{self.loc}{manifestUrl.split('/')[-1]}/"

        if not os.path.isfile(manifestFileName):
            downloaded = self._download_manifest(manifestUrl)
            if os.path.isfile(downloaded):
                zip = zipfile.ZipFile(downloaded, "r")
                zip.extractall(f"./{self.loc}/")
                zip.close()

        self.manifests[language] = manifestFileName

    def _download_manifest(self, url):
        """Downloads a manifest from Bungie and saves it locally.

        Args:
            - **url** (:class:`str`) -
                The url to get the download from.

        Returns:
            - **fileName** (:class:`str`) -
                The file that the manifest was saved to.
        """

        data = requests.get(url, headers = self.headers)
        fileName = f"./{self.loc}/manifest"
        with open(fileName, 'wb') as file:
            file.write(data.content)

        return fileName
