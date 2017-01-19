import json

def printout(actionprofile, response):
        jsondata = jsonfor(response)
        if jsondata != None:
            print( json.dumps( jsondata, indent=2 ) )

def jsonfor(response):
    try:
        return response.json()
    except ValueError as e:
        return None

