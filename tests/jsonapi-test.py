import jsonapi
import testf

testf.equal(
    jsonapi.updateurl("http://mock/$id/$ide/$id/thing",{"id":"ME","ide":"vim"}),
    "http://mock/ME/vim/ME/thing",
    "Replace whole-words in URL"
)
