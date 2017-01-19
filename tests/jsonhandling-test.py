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

testf.equal(
    jh.splitPath("create[]"),
    ["create",""],
    "Single index all"
)

abeta = ["alpha","beta"]
ducktruck = [
        {"munster":"truck"},
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

testf.equal(jh.getData(jsondata, "a"), 1, "Read int" )
testf.equal(jh.getData(jsondata, "b"), abeta, "Read array" )
testf.equal(jh.getData(jsondata, "b[]"), abeta, "Read array explicitly" )
testf.equal(jh.getData(jsondata, "c[1].munster"), "duck", "Read beyond array" )

sorteda = jh.getData(jsondata, "c[].munster")
sorteda.sort()
testf.equal(sorteda , ['duck','truck'], "Read array subitems multiple" )
