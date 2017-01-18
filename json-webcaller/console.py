CDEF='[0m'

from sys import stderr,stdin

def printe(msg):
    stderr.write(msg)
    stderr.write("\n")
    stderr.flush()

def faile(msg):
    printe('[31;1m'+str(msg)+CDEF)

def warne(msg):
    printe('[33;1m'+str(msg)+CDEF)

def infoe(msg):
    printe('[32;1m'+str(msg)+CDEF)

def uask(msg):
    printe(msg)
    return stdin.readline().strip()
