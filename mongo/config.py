import pymongo

# CONNECTION = "mongodb+srv://user:user123@pears.8dysv.mongodb.net/test?authSource=admin&replicaSet=atlas-5hnvbi-shard" \
#              "-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true "
CONNECTION = "mongodb://localhost:27017"
DATABASE = "agas"

_my_client = pymongo.MongoClient(CONNECTION)

_my_db = _my_client[DATABASE]
