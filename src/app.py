from flask import Flask, request, Response
from flask import json
from flask.json import jsonify
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['MONGO_URI']='mongodb://localhost/backend-python-db'
mongo = PyMongo(app)

@app.route('/create-user', methods=['POST'])
def create_user():
    # Reciviendo datos
    # print(request.json)
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    if username and email and password:
        hashedPassword = generate_password_hash(password)
        id = mongo.db.users.insert({
            'username': username, 
            'email': email, 
            'password:': hashedPassword
        })
        response = {
            'id': str(id),
            'username': username,
            'email': email,
            'password': hashedPassword
        }
        return response
    else:
        return not_found()

    return {'message': 'received'}

@app.route('/get-users', methods=['GET'])
def get_users():
    users = mongo.db.users.find()
    response = json_util.dumps(users)
    return Response(response, mimetype='application/json')

@app.route('/get-user', methods = ['GET'])
def get_user():
    userId = request.json['user_id']

    if userId != '':
        user = mongo.db.users.find_one({'_id': ObjectId(userId)})
        response = json_util.dumps(user)
        return Response(response, mimetype='application/json')

@app.route('/delete-user', methods = ['DELETE'])
def delete_user():
    userId = request.json['user_id']
    
    if userId:
        mongo.db.users.delete_one({'_id': ObjectId(userId)})
        response = jsonify({'status': 'Usuario con id: ' + userId + ', eliminado satisfactoriamente.'})
        return response
    else:
        return not_found()

@app.route('/update-user', methods = ['PUT'])
def update_user():
    userId = request.json['user_id']
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    if username and email and password:
        hashedPassword = generate_password_hash(password)
        mongo.db.users.update_one({'_id': ObjectId(userId)}, {'$set': {
                'username': username,
                'email': email,
                'password': hashedPassword 
            }})
        response = jsonify({'status': 'Usuario con id: ' + userId + ', actualizado satisfactoriamente.'})
        return response
        

app.errorhandler(404)
def not_found(error = None):
    response = jsonify({
        'message': 'Recurso no encontrado: ' + request.url,
        'status': 404
    })
    response.status_code = 404
    return response

if __name__ == "__main__":
    app.run(debug=True)