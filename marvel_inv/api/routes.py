from flask import Blueprint, request, jsonify
from marvel_inv.helpers import token_required
from marvel_inv.models import db, Character, hero_schema, heros_schema


api = Blueprint('api', __name__, url_prefix = '/api')


@api.route('/getdata')
@token_required
def getdata(our_user):
    return {'some': 'value'}

#create drone endpoint
@api.route('/heros', methods = ['POST'])
@token_required
def create_character(our_user):
    name = request.json['name']
    description = request.json['description']
    power = request.json['power']
    role = request.json['role']
    identity = request.json['identity']
    sidekick = request.json['sidekick']
    comic = request.json['comic']
    date = request.json['date']
    user_token = our_user.token

    print(f"User Token: {our_user.token}")

    character = Character(name, description, power, role, identity, sidekick, comic, date, user_token=user_token)

    db.session.add(character)
    db.session.commit()

    response = hero_schema.dump(character)

    return jsonify(response)


#Retrieve all drone endpoints
@api.route('/heros', methods = ['GET'])
@token_required
def get_heros(our_user):
    owner = our_user.token
    heros = Character.query.filter_by(user_token= owner).all()
    response = heros_schema.dump(heros)

    return jsonify(response)


#Retrieve One Drone Endpoint
@api.route('/heros/<id>', methods = ['GET'])
@token_required
def get_hero(our_user, id):
    owner = our_user.token
    if owner == our_user.token:
        hero = Character.query.get(id)
        response = hero_schema.dump(hero)
        return jsonify(response)
    else:
        return jsonify({'message': 'Valid Id Required'}), 401
    
#Update Drone Endpoint
@api.route('/heros/<id>', methods = ['PUT','POST'])
@token_required
def update_hero(our_user, id):
    hero = Character.query.get(id)
    hero.name = request.json['name']
    hero.description = request.json['description']
    hero.power = request.json['power']
    hero.role = request.json['role']
    hero.identity = request.json['identity']
    hero.sidekick = request.json['sidekick']
    hero.comic = request.json['comic']
    hero.date = request.json['date']
    hero.user_token = our_user.token

    db.session.commit()
    response = hero_schema.dump(hero)
    return jsonify(response)

#Delete Drone Endpoint
@api.route('/heros/<id>', methods = ['DELETE'])
@token_required
def delete_heros(our_user, id):
    hero = Character.query.get(id)
    db.session.delete(hero)
    db.session.commit()

    response = hero_schema.dump(hero)
    return jsonify(response)