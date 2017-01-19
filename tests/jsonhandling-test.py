import testf
import jsonhandling as jh

testf.equal(jh.splitPath("nothing"), ["nothing"], "Single item path")

testf.equal(
    jh.splitPath("action.create[5].nothing"),
    ["action","create",5,"nothing"],
    "Explicit index path"
)

testf.equal(
    jh.splitPath("action.create[].nothing"),
    ["action","create","","nothing"],
    "Global match path"
)

abeta = ["alpha","beta"]
ducktruck = [
        {"monster":"truck"},
        {"munster":"duck"}
    ]

jsondata = {
    "a":1,
    "b":abeta,
    "c":ducktruck
}

testf.equal(jh.readDataItem(jsondata, "a"), 1, "Read a data item")
testf.equal(jh.readDataItem(jsondata, "b"), abeta, "Return an array from data item")
testf.equal(jh.readDataItem(jsondata['b'], ""), abeta, "Return an array from data item (implicit 'all')")

for path in ["a","b","c[]","c[1].munster"]:
    print("-> "+path)
    print("----> "+ str( jh.readDataTree( jsondata, path ) ))
