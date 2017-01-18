
class RequiredFieldException(Exception):
    def __init__(self,msg):
        Exception.__init__(self,msg)

def datacheck(actionprofile, rdata):
    # TODO - check for a "required" field, and see that rdata has them all
    datakeys = rdata.keys()
    if "requires" in actionprofile.keys():
        for requirement in actionprofile["requires"]:
            if not requirement in datakeys or rdata[requirement] == "" or rdata[requirement] == None:
                raise RequiredFieldException("This action requires a '%s' parameter (all required fields: %s) "%(requirement, ','.join(datakeys) ))
