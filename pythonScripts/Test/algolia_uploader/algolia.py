import sys
import os.path
from algoliasearch import algoliasearch

client = algoliasearch.Client("L9CLTCSBTW", "5c4aa92dcd38c2bd8c99bee0b3444bfa")

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
