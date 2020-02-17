import flask
import json
from flask import jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

users = json.loads(
    '[{"id": 1, "name": "Reginaldo Morais"}, {"id": 2, "name": "John Doe"}]')


@app.route('/users', methods=['GET'])
def list():
    return jsonify(users)

@app.route('/users/<int:id>', methods=['GET'])
def get(id):
    for user in users:
        if user['id'] == id:
            return jsonify(user);
    
    return page_not_found("sss");


@app.errorhandler(404)
def page_not_found(e=None):
    if e:
        print(f'Error: {e}');
    return "<h1>404 - Not Found</h1><p>The resource could not be found.</p>", 404


app.run()
