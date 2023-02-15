from functools import wraps

import secrets
from flask import request, jsonify, json

from marvel_inv.models import User

# import decimal

import requests

from marvel import Marvel 


def token_required(our_flask_function):
    @wraps(our_flask_function)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token'].split(' ')[1]
            print(token)

        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            our_user = User.query.filter_by(token = token).first()
            print(our_user)
            if not our_user or our_user.token != token:
                return jsonify({'message': 'Token is invalid'})

        except:
            owner = User.query.filter_by(token=token).first()
            if token != owner.token and secrets.compare_digest(token, owner.token):
                return jsonify({'message': 'Token is invalid'})
        return our_flask_function(our_user, *args, **kwargs)
    return decorated


# class JSONEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, decimal.Decimal):
#             return str(obj)
#         return super(JSONEncoder, self).default(obj)
    

mar_var = Marvel(PUBLIC_KEY='3bda2f419f70b73208ca0824fcf06ebe', PRIVATE_KEY='af4adb606f137ed541d8916bd5746110d38f3a7a')

characters = mar_var.characters
comics = mar_var.comics 
creators = mar_var.creators 
events = mar_var.events
series = mar_var.series
stories = mar_var.stories
#all(), get(id), comics(id), events(id), series(id), stories(id)