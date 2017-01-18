import jsonfile, sys

jf = jsonfile.JSONFile("demo.json")

if jf.data == None:
    print("FAIL")
else:
    print(jf.data["key"] )

jsonfile.mergeArtefacts(jf.data, sys.argv[1:])

jf.writefile()
