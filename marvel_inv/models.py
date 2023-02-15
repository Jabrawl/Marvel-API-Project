from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid 
from datetime import datetime

#Adding Flask security for passwords
from werkzeug.security import generate_password_hash, check_password_hash

#Import secrets to generate user token
import secrets

#flask login to check for an authenticated user
from flask_login import UserMixin, LoginManager

#import for flask marshmallow
from flask_marshmallow import Marshmallow

#Create an instance of SQLAlchemy
db = SQLAlchemy()
login_manager = LoginManager() #<-- do not forget parenthesis
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = False)
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    # drone = db.relationship('Drone', backref = 'owner', lazy = True)
    

    def __init__(self, email, password, first_name = '', last_name = '', id = '', token = ''):
        self.id = self.set_id()
        self.password = self.set_password(password)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.token = self.set_token(24)
        

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_token(self, length):
        return secrets.token_hex(length)
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash
    
    def __repr__(self):
        return f"User {self.email} has been added to the database!"
    

class Character(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(200))
    power = db.Column(db.String(150))
    role = db.Column(db.String(150))
    identity = db.Column(db.String(150))
    sidekick = db.Column(db.String(150))
    comic = db.Column(db.Integer)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)


    def __init__(self, name, description, power, role, identity, sidekick, comic, user_token, id = ''):
        self.id = self.set_id()
        self.name = name
        self.description = description
        self.power = power
        self.role = role
        self.identity = identity
        self.sidekick = sidekick
        self.comic = comic
        self.user_token = user_token


    def set_id(self):
        return secrets.token_urlsafe()
    
    def __repr__(self):
        return f"The following Character has been added: {self.name}"
    

class HeroSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'description', 'power', 'role', 'identity', 'sidekick', 'comic', 'date']


hero_schema = HeroSchema()
heros_schema = HeroSchema(many=True)