import requests
import jsonfile
import json
import datacheck
import sys
import console
import re

class WebAPIHTTPException(Exception):
    def __init__(self,msg):
        Exception.__init__(self,msg)

def request(key, actionprofile, artefacts, urimodifiers):
    standard_headers = {
        "Authorization": "Bearer "+key,
        "Content-Type": "application/json"
    }
    url = actionprofile["url"]
    method = actionprofile["method"]
    rdata = {}

    # === Build up the data
    if "requestdata" in actionprofile.keys():
        rdata = actionprofile["requestdata"]

    jsonfile.mergeArtefacts( rdata, artefacts )

    try:
        datacheck.datacheck(actionprofile, rdata)
        url = updateurl(url, urimodifiers)

    except datacheck.RequiredFieldException as e:
        console.faile(str(e)+"\n")
        return None

    try:

        response = None

        if method == "GET":
            response = do_get(url,standard_headers)

        elif method == "POST":
            response = do_post(url, standard_headers, rdata)

        elif method == "DELETE":
            response = do_delete(url, standard_headers)

        else:
            raise WebAPIHTTPException("Unsupported HTTP method "+method)

        http_expect_class(200, response)
        print( json.dumps(jsonfor(response), indent=2) )
    except Exception as e:
        console.faile(str(e) )
        exit(127)


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
    return ""

def updateurl(url, rdata):
    for item in rdata:
        patstr = "\\$%s\\b" % (item,)
        founditem = re.match(".*"+patstr, url)
        if founditem:
           url = re.sub(patstr, str(rdata[item]), url)
    return url
