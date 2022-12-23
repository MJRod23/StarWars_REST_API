"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
import requests
import json
#from models import Person



app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/people', methods=['GET'])
def handle_people():
    response = requests.get('https://swapi.dev/api/people')
    return (response.json()["results"]), 200

@app.route('/planets', methods=['GET'])
def handle_planet():
    response = requests.get('https://swapi.dev/api/planets')
    return (response.json()["results"]), 200

@app.route('/people/<people_id>', methods=['GET'])
def handle_id(people_id):
    response = requests.get('https://swapi.dev/api/people/' + people_id)
    return (response.json()), 200

@app.route('/planets/<planet_id>', methods=['GET'])
def handle_planetid(planet_id):
    response = requests.get('https://swapi.dev/api/planets/' + planet_id)
    return (response.json()), 200

@app.route('/users', methods=['GET'])
def handle_users():
    users_query=User.query.all()
    all_users=list(map(lambda x:x.serialize(),users_query))
    return all_users, 200

@app.route('/favorite/planet/<planet_id>/<user_id>', methods=['POST'])
def handle_favorite_planets(planet_id, user_id):
    user1 = User.query.get(user_id)
    if user1 is None:
        user1 = User(id=user_id, favorite_planets=json.dumps([planet_id]), favorite_people=json.dumps([]))
        db.session.add(user1)
        db.session.commit()
        return 'ok', 200

    user1.favorite_planets.append(planet_id)
    db.session.commit()
    return 'ok', 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
