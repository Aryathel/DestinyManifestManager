import sqlite3

class ManifestReader:
    """A reader class meant to read the Destiny 2 API manifests after they are downloaded.

    This reader is used to access all necessary information in the manifests.

    **Parameters**:
        - **manifestFile** (:class:`str`) - The file location of a manifest file to access data from.

    .. note::
        This is an **in development** build, and will likely have many bugs.
    """
    def __init__(self, manifestFile):
        self.connection = sqlite3.connect(manifestFile)
        self.cursor = self.connection.cursor()

    def query(self, hash, definition, identifier):
        """Queries data from a specific location in the manifest.

        Takes the requested activity category, then finds the activity that has an identifier
        matching the hash provided.

        **Parameters**:
            - **hash** (:class:`str`) - The hash of the activity to search for.
            - **definition** (:class:`str`) - The category of activities to search for the given activity hash in.
            - **identifier** (:class:`str`) - The key of the key and hash value pair to search for.

        **Returns**:
            - List [:class:`dict`] - A list containing dictionaries for every valid entry found.
        """
        sql = """
            SELECT json from {0}
            WHERE {1}={2};
        """.format(definition, identifier, hash)

        print(sql)

        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.cursor.close()
        self.connection.close()
