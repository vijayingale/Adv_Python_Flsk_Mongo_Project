import json

import flask_objectid_converter
from flask import Flask
from pymongo import MongoClient
from bson.json_util import dumps
from flask import jsonify,request

from werkzeug.security import generate_password_hash,check_password_hash

app= Flask(__name__)
app.secret_key = 'secretkey'

myclient = MongoClient("mongodb://%s:%s@127.0.0.1" % ('myUserAdmin', 'abc123'))
# #create collection
print("\n\t .Connection Successful : ")
mydb = myclient['test']
collection = mydb['student']


@app.route('/add',methods=['POST'])
def add_user():
    _json = request.get_json()
    print(_json)
    _id = _json['_id']
    _name = _json['name']
    _roll_number = _json['roll_number']
    _branch =_json['branch']
    _marks = _json['marks']

    if request.method == 'POST':
        record = {
                "_id": _id,
                "name": _name,
                "roll_number": _roll_number,
                "branch": _branch,
                "marks": _marks,

            }
        record1 = collection.insert_one(record)
        responce = jsonify("User Added SuccessFully ")

        return responce,201
    else:
        return not_found()

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'ststus': 404,
        'message':'Not Found '+ request.url
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

@app.route('/user')
def user():
    users = collection.find()
    resp = dumps(users)
    return resp


@app.route('/user/<id>')
def Find_single(id):
    users = collection.find({"_id":int(id)})
    dict ={}
    for x in users:
        dict.update(x)
    # print(users)
    print(dict)

    return dumps(dict)


@app.route('/user/<id>', methods=['DELETE'])
def Delete_User(id):
    users = collection.find({"_id":int(id)})
    _json = request.get_json()
    if users != "" and request.method == 'DELETE':
        collection.delete_one({"_id":int(id)})


        return "User Deleted Success Fully",200

@app.route('/user/<id>', methods=['PUT'])
def Update_User(id):
    _id = int(id)
    _json = request.get_json()
    print(_json)
    filter = {"_id": _id}
    for x in _json:
        print("\n",x ,_json[x])
        collection.update_one(filter, {"$set": {x: _json[x]}})


    return "User Updated Successfully ",200



if __name__ == '__main__':
    app.run(debug=True)
