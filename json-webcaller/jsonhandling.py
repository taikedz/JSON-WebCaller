import json
import re

MREAD = 1
MWRITE = 2

class JSONPathException(Exception):
    def __init__(self,msg):
        Exception.__init__(self, msg)

class InvalidPathException(Exception):
    def __init__(self,msg):
        Exception.__init__(self, msg)

def mergeArtefacts(jsondata, artefacts):
    ''' Merge a bunch of json.path.key=value items into the specified jsondata
    '''
    for apath in artefacts.keys():
        value = artefacts[apath]
        writePath(jsondata, apath, value)

def writePath(jsondata, path, datavalue):
    ''' For the given json data, write a new value to the specified path
    '''
    drillToDataPoint(MWRITE, jsondata, path, datavalue)

def readPath(jsondata, path):
    ''' Read the json data on the specified path
    '''
    return drillToDataPoint(MREAD, jsondata, path)

# TODO -- add a mode that forces the creation of a new element (for write mode)
def descend(data, thekey, action=None):
    if (type(data) == dict and thekey in data.keys()) or (type(data) == list and thekey < len(data) ):
        return data[thekey]
    raise InvalidPathException("Could not descend to "+str(thekey))

def drillToDataPoint(action, jsondata, path, datavalue=None):
    ''' Drill down to the data element on the path, and either return it or set a new value
    '''
    steps = path.split(".")
    locus = jsondata
    maxi = len(steps)

    for i in range(0, maxi ):
        step = steps[i]
        if step[-1] == ']':
            m = re.match("([a-zA-Z0-9]+)\[([0-9]*)\]$", step)
            if m == None:
                raise JSONPathException("Could not extract index on section "+step)
            locus = descend( locus, m.group(1), action )
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

def readDataTree(jsondata, path):
    '''Drill down the data tree, finding matches
    '''
    newdata = {}
    ndatacursor = newdata
    datacursor = jsondata

    steps = splitPath(path)

    while len(steps) > 0:
        step = steps.pop(0)
        target = readDataItem(datacursor, step)
        datacursor = datacursor[step]

        if type(target) == list:
            ndatacursor[step] = []
            ndatacursor = ndatacursor[step]
            for item in target:
                ndatacursor.append( readDataTree(item, steps[:] ) )
            return newdata
        else:
            ndatacursor[step] = target
            ndatacursor = ndatacursor[step]

    return newdata

def splitPath(path):
    if type(path) == list:
        return path
    if path.find("..") >= 0:
        raise JSONPathException("Cannot have consecutive '.' joiners (%s)"%(path,))

    steps = path.split(".")
    newsteps = []

    for s in steps:
        m = re.match("([a-zA-Z0-9_]+)\[([0-9]*)\]$", s)
        if m == None:
            newsteps.append(s)
        else:
            newsteps.append(m.group(1))
            if m.group(2) != "":
                newsteps.append(int(m.group(2)) )
            else:
                newsteps.append("")
    return newsteps

def readDataItem(jsondata, step):
    '''Given the data, and a step, return the appropriate result
    '''
    target = None
    print("Read %s from %s"%(step,str(jsondata)))

    try:
        if step == "":
            target = jsondata

        else:
            target = jsondata[step]

    except IndexError as e:
        raise JSONPathException(e)

    return target
    
