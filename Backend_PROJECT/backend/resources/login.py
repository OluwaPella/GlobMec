from flask import request , jsonify
from models import User 
from flask_bcrypt import Bcrypt
from flask_restful import Resource
from session  import create_session

class LoginResource(Resource):
    def post(self):
        data = request.json
        email = data.get("email")
        password = data.get("password")
        
        user = User.query.filter_by(email=email).first()
        if user and Bcrypt.check_password_hash(user.password, password):
            new_session = create_session(user.id)
            return jsonify(new_session,"login successfully"), 200
        return jsonify({"error": "Invalid email or password"}), 401