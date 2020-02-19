import flask
import json
from flask import jsonify, request
from flask_pymongo import PyMongo
from functools import wraps

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config["MONGO_URI"] = "mongodb://localhost:27017/demo"
mongo_client = PyMongo(app)


# users = json.loads(
#    '[{"id": 1, "name": "Reginaldo Morais"}, {"id": 2, "name": "John Doe"}]')


def validate_json(*expected_args):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            json_ob = request.get_json()
            for expected_arg in expected_args:
                if expected_arg not in json_ob or json_ob.get(expected_arg) is None:
                    return bad_request(f'Field [{expected_arg}] is required')
            return func(*args, **kwargs)
        return wrapper
    return decorator


@app.route('/users', methods=['GET'])
def list():
    users = [user for user in mongo_client.db.users.find()]
    return jsonify(users), 200


@app.route('/users/<int:id>', methods=['GET'])
def get(id):
    user = mongo_client.db.users.find_one({"_id": id})
    if (user):
        return user, 200
    return page_not_found()


@app.route('/users', methods=['POST'])
@validate_json("_id", "name")
def post():
    data = request.get_json()
    user = mongo_client.db.users.find_one({"_id": data['_id']})
    if user == None or user['_id'] != data['_id']:
        userId = mongo_client.db.users.save(data)
        return jsonify(mongo_client.db.users.find_one({"_id": userId})), 201
    return bad_request()


@app.route('/users/<int:id>', methods=['PUT'])
@validate_json("name")
def put(id):
    data = request.get_json()
    user = mongo_client.db.users.find_one({"_id": id})
    if user != None and user['_id'] == id:
        user['name'] = data['name']
        mongo_client.db.users.update_one(
            {'_id': id}, {'$set': {'name': data['name']}})
        return jsonify(mongo_client.db.users.find_one({"_id": id})), 200
    return page_not_found()


@app.route('/users/<int:id>', methods=['DELETE'])
def delete(id):
    user = mongo_client.db.users.find_one({"_id": id})
    if user != None and user['_id'] == id:
        db_response = mongo_client.db.users.delete_one({"_id": id})
        return "", 204
    return page_not_found()


@app.errorhandler(400)
def bad_request(e=None):
    if e:
        print(f'Error: {e}')
        return jsonify({"Error": e}), 400
    return "", 400


@app.errorhandler(404)
def page_not_found(e=None):
    if e:
        print(f'Error: {e}')
    return "<h1>404 - Not Found</h1><p>The resource could not be found.</p>", 404


app.run()
