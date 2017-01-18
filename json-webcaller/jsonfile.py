import json
import re
import console

MREAD = 1
MWRITE = 2

class JSONPathException(Exception):
    def __init__(self,msg):
        Exception.__init__(self, msg)

class InvalidPathException(Exception):
    def __init__(self,msg):
        Exception.__init__(self, msg)

class JSONFile:

    def __init__(self, path):
        self.path = path
        self.readfile()

    def readfile(self):
        fh = open(self.path,'r')
        self.data = json.loads( ''.join(fh.readlines()) )
        fh.close()

    def get(self, qpath):
        return readPath(self.data, qpath)

    def set(self, qpath, data):
        writePath(self.data, qpath, data)

    def writefile(self):
        fh = open(self.path, 'w')
        jsonstring = json.dumps(self.data,indent=4).replace("    ","\t")
        fh.write( jsonstring )
        fh.flush()
        fh.close()

# Supporting functions

def mergeArtefacts(jsondata, artefacts):
    ''' Merge a bunch of json.path.key=value items into the specified jsondata
    '''
    for item in artefacts:
        apath, value = item.split('=',1)
        writePath(jsondata, apath, value)

def writePath(jsondata, path, datavalue):
    ''' For the given json data, write a new value to the specified path
    '''
    drillToData(MWRITE, jsondata, path, datavalue)

def readPath(jsondata, path):
    ''' Read the json data on the specified path
    '''
    return drillToData(MREAD, jsondata, path)

# TODO -- add a mode that forces the creation of a new element (for write mode)
def descend(data, thekey):
    if (type(data) == dict and thekey in data.keys()) or (type(data) == list and thekey < len(data) ):
        return data[thekey]
    raise InvalidPathException("Could not descend to "+str(thekey))

def drillToData(action, jsondata, path, datavalue=None):
    ''' Drill down to the data element on the path, and either return it or set a new value
    '''
    steps = path.split(".")
    locus = jsondata
    maxi = len(steps)

    for i in range(0, maxi ):
        step = steps[i]
        if step[-1] == ']':
            m = re.match("([a-zA-Z0-9]+)\[([0-9]+)\]$", step)
            if m == None:
                raise JSONPathException("Could not extract index on section "+step)
            locus = descend( locus, m.group(1) )
            step = int(m.group(2))


        if i+1 < maxi:
            locus = descend(locus, step )
            continue

        target = descend(locus, step)
        if action == MREAD:
            return target

        elif action == MWRITE:
            locus[step] = datavalue

        else:
            raise JSONDataHandleException("Unknown operation")

