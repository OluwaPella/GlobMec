from models import User, Address, db
from flask import request, make_response, jsonify
from flask_restful import Resource
from flask_jwt_extended import  create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt() 

class RegisterResource(Resource):
    def post(self):
        data = request.json


        existing_user = User.query.filter(User.email == data.get('email')) and User.query.filter(User.contact == data.get('contact')).first()
        if existing_user:
            return make_response(jsonify({"message": "User  or contacts already exists"}), 400)

        password = data.get('password')
        if not all([data.get('name'), data.get('last_name'), data.get('email'), password, data.get('gender'), data.get('contact'), data.get('country'), data.get('services_offered')]):
            return  make_response(jsonify({'message': 'Incomplete details'}), 401)
        elif any(c.isalpha() for c in password) and any(c.isdigit() for c in password): 
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        else:
            return make_response(jsonify({'message': 'Password must contain at least one letter and one number'}), 401)

        new_user = User(
                name=data.get('name'),
                last_name=data.get('last_name'),
                email=data.get('email'),
                password=hashed_password,
                gender=data.get('gender'),
                contact=data.get('contact'),
                services_offered=data.get('services_offered')
        )
        new_user_address = Address(
                country=data.get('country'),
                city=data.get('city'),
                state=data.get('state'),
                provinces=data.get('provinces'),
                districts=data.get('districts'),
                zipcode = data.get('zipcode')
                )
        
        new_user.addresses = [new_user_address]
        new_user_address.user = new_user
        db.session.add(new_user)
        db.session.commit()
        
        return make_response(jsonify({'message': 'Register successful'}), 201)
class LoginResource(Resource):
    def post(self):
        data = request.json
        email = data.get("email")
        password = data.get("password")
        
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            refresh = create_refresh_token(identity=user.id)
            access = create_access_token(identity=user.id)

            return make_response(jsonify({
                'user': {
                    'refresh' : refresh,
                    'access' : access,
                    'name' : user.name,
                    'email' : user.email
                }
            
            }), 200)
        
        return make_response(jsonify({"error": "Invalid email or password"}), 401)

class LogoutResource(Resource):
    def post(self):
        
        return {'message': 'Successfully logout' }, 200
    
class UsersResource(Resource):
    def get(self):
        users = User.query.all()

        user_list = []

        for user in users:
            user_dict = {
            'id': user.id,
            'name': user.name,
            'last_name': user.last_name,
            'email': user.email,
            'gender': user.gender,
            'contact': user.contact,
            'services_offered': user.services_offered,
            'address': {
                'country': user.address.country if user.address else None,
                'city': user.address.city if user.address else None,
                'districts': user.address.districts if user.address else None,
                'provinces': user.address.provinces if user.address else None,
                'street': user.address.street if user.address else None,
                'state': user.address.state if user.address else None,
                'zipcode': user.address.zipcode if user.address else None
                }  if user.address else None
            }
            user_list.append(user_dict)

        return jsonify({'users': user_list})


class SearchResource(Resource):
    def get(self):
        country = request.args.get('country')
        state = request.args.get('state')
        city  = request.args.get('city')
        provinces = request.args.get('provinces')
        districts = request.args.get('country')
        name = request.args.get('name')

        user_query = User.query

        if country :
              user_query =  user_query.filter(User.address.has(country=country))
        if state :
             user_query =  user_query.filter(User.address.has(state=state))
        if city :
            user_query =  user_query.filter(User.address.has(state=state))
        if  provinces :
            user_query =  user_query.filter(User.address.has(provinces= provinces))
        if  districts :
            user_query =  user_query.filter(User.address.has(districts= districts))
        if name :
            user_query.filter(User.name.ilike(f"%{name}%"))

        users =  user_query.all()

        return jsonify({'user': users}), 200
    
