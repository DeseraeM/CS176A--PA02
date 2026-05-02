# What Needs to Be Built:
#   get()  — given a filepath (relative to the server root):
#              • if it's a file, return its contents as bytes
#              • if it's a directory, return a simple HTML page as bytes:
#                    <html><body><h1>/the/path</h1></body></html>
#              • if it does not exist, return None
#   head() — same logic as get(), but return the byte count (int) instead
#            of the contents, or None if the path does not exist
class FileReader:
    def __init__(self):
        pass

    def get(self, filepath, cookies):
        """
        Returns a binary string of the file contents, or None.
        """
        return None

    def head(self, filepath, cookies):
        """
        Returns the size to be returned, or None.
        """
        return None
