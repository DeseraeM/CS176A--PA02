# What Needs to Be Built:
#   get()  — given a filepath (relative to the server root):
#              • if it's a file, return its contents as bytes
#              • if it's a directory, return a simple HTML page as bytes:
#                    <html><body><h1>/the/path</h1></body></html>
#              • if it does not exist, return None
#   head() — same logic as get(), but return the byte count (int) instead
#            of the contents, or None if the path does not exist
import os

class FileReader:
    def __init__(self,file_path):
        self.file_path = file_path

    def get(self, file_path, cookies):
        """
        Returns a binary string of the file contents, or None.
        """
        #checks if its a file
        decodeFile = file_path.decode()
        joined = os.path.join(self.file_path, decodeFile)
        if os.path.exists(joined):
            if os.path.isfile(joined):
                read = open(joined,"rb")
                fileC = read.read()
                read.close()
                return fileC
            if os.path.isdir(joined):
                result = ""
                directoryF = os.listdir(joined)
                for d in directoryF:
                    result += f"<li> {d} </li>"
                return f"<html><body><ul> {result} </ul></body></html>".encode()
        else: 
            return None

    def head(self, file_path, cookies):
        """
        Returns the size to be returned, or None.
        """
        decodeFile = file_path.decode()
        joined = os.path.join(self.file_path, decodeFile)
        if os.path.exists(joined):
            if os.path.isfile(joined): 
                read = open(joined,"rb")
                size = len(read.read())
                read.close()
                return size
            if os.path.isdir(joined):
                return len(self.get(joined.encode(), cookies))
        else:
            return None
