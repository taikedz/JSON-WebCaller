import jsonapi
import testf
import console

testf.equal(
    jsonapi.updateurl("http://mock/$id/$ide/$id/thing",{"id":"ME","ide":"vim"}),
    "http://mock/ME/vim/ME/thing",
    "Replace whole-words in URL"
)

try:
    jsonapi.updateurl("http://thing/$id", {"not":"applicable"})
    console.faile("FAIL Prevent unmet substitutions")
except jsonapi.WebAPIHTTPException:
    console.infoe("PASS Prevent unmet substitutions")
    
