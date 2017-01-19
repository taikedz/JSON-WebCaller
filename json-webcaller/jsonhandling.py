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
    if action == MREAD and (type(data) == dict and thekey in data.keys()) or (type(data) == list and thekey < len(data) ):
        return data[thekey]
    elif action == MWRITE:
        data[thekey] = {}
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

def getData(jsondata, path):
    steps = splitPath(path)
    return readDataTree(jsondata, steps)

def writeDataPoint(jsondata, steps, value):
    '''Drill down the data tree, and write the property at that location

    INCOMPLETE
    '''
    newdata = jsondata

    for i in range(0,len(steps) ):
        s = steps[i]
        # if the item ends with [] or {}, create appropriate structure
        if s[:-2] == '{}':
            addDataStructure(newdata, s[:-2], {})
        elif s[:-2] == '[]':
            addDataStrcuture(newdata, s[:-2], [])
        elif s != "":
            newdata = newdata[s]
        else:
            array = newdata
            newdata = []
            for item in array:
                newdata.append( readDataTree(item, steps[i+1:]) )
            # at this point we have consumed the steps
            return newdata

    return newdata

def addDataStructure(jsondata, label, newsubdata):
    '''INCOMPLETE'''
    if type(jsondata) == list:
        if type(label) == int:
            jsondata[label] = newsubdata
        elif
        jsondata.append(newsubdata)

def readDataTree(jsondata, steps):
    '''Drill down the data tree, until the match is found. Return the data structure at t he locaiton specified.
    '''
    newdata = jsondata

    for i in range(0,len(steps) ):
        s = steps[i]
        print("Lookup %s"%(s,))
        if s != "":
            newdata = newdata[s]
        else:
            array = newdata
            newdata = []
            for item in array:
                newdata.append( readDataTree(item, steps[i+1:]) )
            # at this point we have consumed the steps
            return newdata

    return newdata

def splitPath(path):
    # FIXME - what about nested arrays -- a[][].b ?
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
                newsteps.append("") # FIXME nested arrays are somewhere here
    return newsteps
