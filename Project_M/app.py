from flask import Flask
from flask_restful import Api
from backend.resources.auth import RegisterResource, LoginResource, LogoutResource, SearchResource, UsersResource
from flask_bcrypt import Bcrypt
from config import Config
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from models import db 

app = Flask(__name__)
CORS(app) 
app.config.from_object(Config)

db.init_app(app)
bcrypt = Bcrypt(app)
jWT = JWTManager(app)


with app.app_context():
    db.create_all()


api = Api(app)
api.add_resource(RegisterResource, '/api/auth/register')
api.add_resource(LoginResource, '/api/auth/login')
api.add_resource(LogoutResource, '/api/auth/logout')
api.add_resource(SearchResource, '/api/auth/Search')
api.add_resource(UsersResource, '/api/auth/Users')




if __name__ == '__main__':
    app.run(debug=False, port=5001)
    
