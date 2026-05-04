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
        #checks if its a file
        if os.path.exists(filepath):
            if os.path.isfile(filepath):
                read = open(filepath,"rb")
                read.close()
                return read.read()
            if os.path.isdir(filepath):
                result = ""
                directoryF = os.listdir(filepath)
                for d in directoryF:
                    result += f"<li> {d} </li>"
                return f"<html><body><ul> {result} </ul></body></html>"
        else: 
            return None

    def head(self, filepath, cookies):
        """
        Returns the size to be returned, or None.
        """
        if os.path.exists(filepath):
            if os.path.isfile(filepath): 
                read = open(filepath,"rb")
                size = len(read.read())
                read.close()
                return size
            if os.path.isdir(filepath):
                return len(self.get(filepath))
        else:
            return None
