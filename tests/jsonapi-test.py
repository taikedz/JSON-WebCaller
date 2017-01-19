from jwcjson import api
import testf
import console

testf.equal(
    api.updateurl("http://mock/$id/$ide/$id/thing",{"id":"ME","ide":"vim"}),
    "http://mock/ME/vim/ME/thing",
    "Replace whole-words in URL"
)

try:
    api.updateurl("http://thing/$id", {"not":"applicable"})
    console.faile("FAIL Prevent unmet substitutions")
except api.WebAPIHTTPException:
    console.infoe("PASS Prevent unmet substitutions")
    
