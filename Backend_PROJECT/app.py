from flask import Flask
from flask_restful import Api
from backend.resources.auth import RegisterResource, LoginResource, LogoutResource, SearchResource, UsersResource, BookingResource, jwt, bcrypt, mail
from config import Config
from flask_cors import CORS
from models import db 

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    CORS(app)

    with app.app_context():
        db.create_all()


    api = Api(app)
    api.add_resource(RegisterResource, '/api/auth/register')
    api.add_resource(LoginResource, '/api/auth/login')
    api.add_resource(LogoutResource, '/api/auth/logout')
    api.add_resource(SearchResource, '/api/auth/Search')
    api.add_resource(UsersResource, '/api/auth/Users')
    api.add_resource(BookingResource,'/api/auth/Booking')


    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=False, port=5001)