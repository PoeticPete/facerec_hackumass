from algoliasearch import algoliasearch

client = algoliasearch.Client("Z1D550ZJE1", "b96d40a815cdb3a9dfaf93d3d0db7749")

index = client.init_index("test_easylock_savedFrames")
# res = index.search("query string")
# res = index.search("query string", { "attributesToRetrieve": "firstname,lastname", "hitsPerPage": 20})
res = index.add_objects([{"objectID": "myID1",
                         "firstname": "Jimmie",
                         "lastname": "Barninger"},
                        {"objectID": "myID2",
                         "firstname": "Warren",
                         "lastname": "Speach"}])
print(res)
