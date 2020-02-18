import flask
import json
from flask import jsonify, request
from functools import wraps

app = flask.Flask(__name__)
app.config["DEBUG"] = True


users = json.loads(
    '[{"id": 1, "name": "Reginaldo Morais"}, {"id": 2, "name": "John Doe"}]')


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
    return jsonify(users)


@app.route('/users/<int:id>', methods=['GET'])
def get(id):
    for user in users:
        if user['id'] == id:
            return jsonify(user)

    return page_not_found()


@app.route('/users', methods=['POST'])
@validate_json("id", "name")
def post():
    data = request.get_json()

    for user in users:
        if user['id'] == data['id']:
            return bad_request("")

    users.append(data)

    return jsonify(users)


@app.route('/users/<int:id>', methods=['PUT'])
@validate_json("name")
def put(id):
    data = request.get_json()
    for user in users:
        if user['id'] == id:
            user['name'] = data['name']
            return jsonify(user)

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
