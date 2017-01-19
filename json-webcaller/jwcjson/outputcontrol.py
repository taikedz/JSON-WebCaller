import json
import re

# output: section, filter, patterns

class OutputFilterException(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)

def printout(actionprofile, response):
    if "output" in actionprofile.keys():
        outputprofile = actionprofile["output"]

        if "section" in outputprofile.keys():
            sectionname = outputprofile["section"]

            if sectionname == "body":
               filterjson(response, outputprofile)

            elif sectionname == "headers":
                filterheaders(response, outputprofile)

            else:
                raise OutputFilterException("Unknown section requested '%s'"%(sectionname,))

        else:
            raise OutputFilterException("No section defined.")
            # or maybe we just return a JSON object with both items as children?


def filterjson(response, outputprofile):
    jsondata = jsonfor(response)
    if jsondata != None:
        print( json.dumps( jsondata, indent=2 ) )
    else:
        raise OutputFilterException("No JSON data!")

def filterheaders(response, outputprofile):
    datafilter = getFilterProfile(outputprofile, ["grep"])
    headers = datafilter.filter(response.headers)

    for hkey in headers:
        print("%s: %s"%(hkey, headers[hkey]))

def getFilterProfile(outputprofile, acceptablefilters):
    if "filter" in outputprofile.keys() and "pattern" in outputprofile.keys():
        if outputprofile["filter"] == "grep":
            return GrepFilter(outputprofile["pattern"])

    return DefaultFilter()

def jsonfor(response):
    try:
        return response.json()
    except ValueError as e:
        return None


class DefaultFilter:
    def __init__(self, pattern=None):
        self.pattern = pattern

    def filter(self,data):
        return data

class GrepFilter(DefaultFilter):
    def __init__(self, pattern):
        DefaultFilter.__init__(self, pattern)
        self.matcher = ".*"+pattern

    def filter(self, data):
        newdata = {}
        for hkey in data:
            if re.match(self.matcher, hkey) or re.match(self.matcher, data[hkey]):
                newdata[hkey] = data[hkey]
        return newdata
