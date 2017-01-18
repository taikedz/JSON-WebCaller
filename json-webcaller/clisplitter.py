def splitout(arguments):
    artefacts = {}
    urimodifiers = {}

    for arg in arguments:
        key,val = arg.split('=',1)

        if key[0] == '%':
            urimodifiers[key[1:]] = val
        else:
            artefacts[key] = val
    return artefacts, urimodifiers
