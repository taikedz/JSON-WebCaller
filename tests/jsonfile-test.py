import jsonfile
import sys
import testf
import console

jf = jsonfile.JSONFile("demo.json")
if not testf.equal( jf.data != None, True, "Data file read"):
    exit(1)

testf.equal(jf.get("key") , "mykey", "First level data was read")
testf.equal(jf.get("actions.destroy.requires[0]") , "id", "Nested value was read")

try:
    jf.get("actions.delete")
    console.faile("FAIL Descend into non-existent branch on read")
except jsonfile.InvalidPathException as e:
    console.infoe("PASS Descend into non-existent branch on read")

jsonfile.mergeArtefacts(jf.data, ["actions.create=newdata"])
testf.equal(jf.data["actions"]["create"], "newdata", "Assign new values")

jf.writefile()
fh = jsonfile.JSONFile("demo.json")
testf.equal(fh.get("actions.create"), "newdata", "Write out did write out")
