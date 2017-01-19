import json
import jsonhandling
import re
import console

class JSONFile:

    def __init__(self, path):
        self.path = path
        self.readfile()

    def readfile(self):
        fh = open(self.path,'r')
        self.data = json.loads( ''.join(fh.readlines()) )
        fh.close()

    def get(self, qpath):
        return jsonhandling.readPath(self.data, qpath)

    def set(self, qpath, data):
        jsonhandling.writePath(self.data, qpath, data)

    def writefile(self):
        fh = open(self.path, 'w')
        jsonstring = json.dumps(self.data,indent=4).replace("    ","\t")
        fh.write( jsonstring )
        fh.flush()
        fh.close()

