from pymongo import MongoClient
from flask import Flask, request, jsonify, redirect, url_for
from functools import wraps

app = Flask(__name__)
client = MongoClient('mongodb://mongodb-server:27017/')
db = client.test
print(client.list_database_names())

def authorize(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.args.get('user', '') != 'hsahu':
            # redirect to login url if user us not authorized
            return redirect(url_for('login', next=request.url))
        return func(*args, **kwargs)
    return wrapper

@app.route('/login', methods=['GET'])
def login():
    return jsonify({
        'authorized': True,
        'message': "redirect url after login: " + request.args.get('next', "")
    })

@app.route('/', methods=['GET'])
@authorize
def root():
    serverStatusResult = db.list_collection_names()
    return str(serverStatusResult)

@app.route('/users', methods=['GET', 'POST'])
@authorize
def get_users():
    if request.method == 'GET':
        data = [x for x in db.users.find({}, { '_id': False})]
        print(data)
        return jsonify({'data': data})
    if request.method == 'POST':
        data = request.get_json(force=True)
        response = db.users.insert(data)
        print(response)
        return jsonify({'status': True})

@app.route('/hello')
def hello_world():
    return "<h1>This is hello world route</h1>\n"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)