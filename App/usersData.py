from config import client, my_database
from app import app
from flask import request, make_response, jsonify
from bson.json_util import dumps
import json
import random

# Creating a collection (table) for our bank api
collection = my_database['bankusers']

# Dsiplaying a welcome message to ensure that flask is working correctly
@app.route("/")
def index():
    return '<h1>Hello World</h1>'

# Inserting user data documents in mongodb one by one
@app.route("/setuserdata", methods = ["POST"])
def insert_one_record():
    input_data = dumps(request.get_json())
    my_dict = json.loads(input_data)
    acc_no = random.randint(10000000, 99999999)
    my_dict["account_number"] = acc_no
    collection.insert_one(my_dict)

    return make_response(jsonify( { "Your account number": acc_no } ))

# Retrieving all the inserted documents from mongodb
@app.route("/getuserdata", methods = ["GET"])
def display_records():
    documents = collection.find({}, {"_id": 0})

    if documents.count() != 0:
        response = dumps([document for document in documents])
        return response, 200
    else:
        return make_response(jsonify( { "error": "User not found" } ), 404)

# retrieves a particular document from database based on bank user's full name
# URl should be http://127.0.0.1:5000/retrieveuserdata?fname=Kartik&lname=Kashyap
@app.route("/retrieveuserdata", methods = ["GET"])
def retrieve_record():
    fname = request.args.get('fname')
    lname = request.args.get('lname')
    full_name = fname + ' ' + lname

    target_record = collection.find( { "name": full_name }, {"_id": 0})

    if target_record.count() != 0:
        response = dumps(target_record)
        return response, 200
    else:
        return make_response(jsonify( { "error": "User not found" } ), 404)

# deletes a bank user record only if correct bank account if given
@app.route("/deleteuserdata/<acc_no>", methods = ["DELETE"])
def delete_record(acc_no):
    target_record = collection.find_one( { "account_number": int(acc_no) } )

    if target_record:
        collection.delete_one( { "account_number": int(acc_no) } )
        return make_response(jsonify( { "message": "Record deleted successfully." } ), 200)
    else:
        return make_response(jsonify( { "error": "User not found" } ), 404)

# updates a bank user record based on his bank account number
@app.route("/updateuserdata/<acc_no>", methods = ["PUT"])
def update_record(acc_no):
    data = request.get_json()

    record = collection.find_one( { "account_number": int(acc_no) } )

    if record:
        collection.update_one( { "account_number": int(acc_no) }, { "$set": data } )
        return make_response(jsonify( { "message": "Record Updated Successfully." } ), 200)
    else:
        return make_response(jsonify( { "error": "User not found" } ), 404)

