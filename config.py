from pymongo import MongoClient
myclient = MongoClient("mongodb://%s:%s@127.0.0.1" % ('myUserAdmin', 'abc123'))
# #create collection
print("\n\t .Connection Successful : ")
mydb = myclient['test']