import requests, jsonfile, json, datacheck, sys, console

class WebAPIHTTPException(Exception):
    def __init__(self,msg):
        Exception.__init__(self,msg)

def request(key, actionprofile, artefacts):
    standard_headers = {
        "Authorization": "Bearer "+key,
        "Content-Type": "application/json"
    }
    url = actionprofile["url"]
    method = actionprofile["method"]
    rdata = {}
    if "requestdata" in actionprofile.keys():
        rdata = actionprofile["requestdata"]

    jsonfile.mergeArtefacts( rdata, artefacts )

    try:
        datacheck.datacheck(actionprofile, rdata)

        response = None

        if method == "GET":
            response = do_get(url,standard_headers)
        elif method == "POST":
            response = do_post(url, standard_headers, rdata)
        elif method == "DELETE":
            response = do_delete(url+"/"+rdata["id"], standard_headers)
        else:
            raise WebAPIHTTPException("Unsupported HTTP method "+method)

        http_expect_class(200, response)
        print( json.dumps(jsonfor(response), indent=2) )
    except datacheck.RequiredFieldException as e:
        sys.stderr.write(str(e)+"\n")
        sys.stderr.flush()


def do_get(url,headers):
    return requests.get(
        url,
        headers=headers
        )

def do_delete(url,headers):
    return requests.delete(
        url,
        headers=headers
        )

def do_post(url, headers, data):
    return requests.post(
        url,
        headers=headers,
        data = json.dumps(data)
        )

def http_expect_class(classnum, responseobject):
    if responseobject.status_code - responseobject.status_code % 100 != classnum:
        raise WebAPIHTTPException(responseobject.reason+" // "+responseobject.text)

def jsonfor(response):
    try:
        return response.json()
    except ValueError as e:
        console.printe(str(e) )
    return {"status":response.status_code}
