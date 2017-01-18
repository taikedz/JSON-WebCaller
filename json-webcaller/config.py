from os import path

def getConfigPath(fpath, dirfile):
    # TODO - translate "~" into home dir when on Windows
    if path.isdir(fpath):
        fpath = fpath+"/"+dirfile

    # TODO detect Windows, replace / with \
    if not path.isfile(fpath):
        raise IOError(fpath + " could not be opened.")

    return fpath

