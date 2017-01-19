import console

console.warne("Tester loaded")

def equal( gotval, targetval, testname ):
    if gotval == targetval:
        console.infoe("PASS "+testname)
        return True
    else:
        console.faile("FAIL %s - got: %s"%(testname, str(gotval)))
        return False
