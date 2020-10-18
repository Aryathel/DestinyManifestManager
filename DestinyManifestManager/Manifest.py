"""
.. module:: Manifest
    :platform: Unix, Windows
    :synopsis: The Destiny 2 API manifest manager.
"""

# Stdlib imports
import json
import os
import zipfile

# 3rd Party Imports
import requests

# Local imports
from .Errors import LocaleException
from .ManifestReader import ManifestReader

# Some general constantsc
D2_API_BASE = "https://www.bungie.net/Platform"
D2_MANIFEST = D2_API_BASE + "/Destiny2/Manifest/"

class Manifest:
    """A manager built to function with the Destiny 2 Bungie API Manifests.

    The manager is used to download, update, and organize manifests for game data from Destiny 2.
    Bungie makes these available publicly through their api.

    **Keyword Parameters**:
        - **loc** (Optional[:class:`str`]) - The folder to store manifest data in.
        - **headers** (Optional[:class:`dict`]) - A dict of headers to attach to any requests.

    .. note::
        This is an **in development** build, and will likely have many bugs.

    """
    def __init__(self, loc=None, headers=None):
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
            - **language** (:class:`str`) - The language locale.

        **Raises**:
            - :class:`LocaleException` - An error in accessing the provided locale.
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

    def decode_hash(self, hash, category, language):
        """Gets the decoded data for a given activity hash.

        Given an activity hash, the activity category, and the locale of the user,
        this function will retrieve information on the activity.

        **Parameters**:
            - **hash** (:class:`str`) - The actual activity hash.
            - **category** (:class:`str`) - The category of activity that the activity the hash relates to belongs in.
            - **language** (:class:`str`) - The shorthand locale identifier for the language to retrieve the activity for.

        **Returns**:
            - Optional[:class:`str`] -
                A string identifying the name of the activity.

        **Raises**:
            - :class:`LocaleException` - An error in accessing the provided locale.
        """
        language = language.lower()
        if self.manifests.get(language, None) == None:
            raise LocaleException(f"Language {language} not found.")
        elif self.manifests.get(language, None) == "":
            self.update_manifest(language)

        if category == "DestinyHistoricalStatsDefinition":
            hash = f"\"{hash}\""

        hash = self._bump_hash(hash)
        identifier = "id"

        with ManifestReader(self.manifests.get(language)) as reader:
            res = reader.query(hash, category, identifier)

        if len(res) > 0:
            return json.loads(res[0][0])

        return None

    def _download_manifest(self, url):
        """Downloads a manifest from Bungie and saves it locally.

        Args:
            - **url** (:class:`str`) - The url to get the download from.

        Returns:
            - :class:`str` - The file that the manifest was saved to.
        """

        data = requests.get(url, headers = self.headers)
        fileName = f"./{self.loc}/manifest"
        with open(fileName, 'wb') as file:
            file.write(data.content)

        return fileName
