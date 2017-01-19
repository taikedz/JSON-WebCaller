
        jsondata = jsonfor(response), indent=2
        if jsondata != None:
            print( json.dumps( jsondata ) )
def jsonfor(response):
    try:
        return response.json()
    except ValueError as e:
        return None

