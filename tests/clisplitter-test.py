import clisplitter
import testf

artefacts, urimodifiers = clisplitter.splitout(["dparam=datathing","%uparam=uristuff","dparam.stuff=values=more"])

testf.equal(len(artefacts) , 2, "Two artefacts")
testf.equal(artefacts["dparam"], "datathing", "Data lookup 1")
testf.equal(artefacts["dparam.stuff"], "values=more", "Lookup two with '=' sign")

testf.equal(len(urimodifiers), 1, "One URI modifier")
testf.equal(urimodifiers["uparam"], "uristuff", "Properly extracted uri parameter")
