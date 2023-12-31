from models import User, Address, db, TokenBlocklist, Booking
from flask import request, make_response, jsonify
from flask_restful import Resource
from flask import flash
from flask_mail import Message, Mail
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
jwt = JWTManager()
mail = Mail()

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
            access_token = create_access_token(identity=user.name)

            flash("Login successful", "success")
            return make_response(jsonify({
                "Successful login": {
                    "access_token" : access_token,
                    'name' : user.name,
                    'email' : user.email
                    }
            }), 200)
        flash("Invalid email or password", "error")
        return make_response(jsonify({"error": "Invalid email or password"}), 401)
      

class LogoutResource(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        jTi = get_jwt()['jti']
        if not TokenBlocklist.is_jti_in_blocklist(jTi):
            token_blocklist = TokenBlocklist(jti=jTi)
            token_blocklist.save()
            return make_response(jsonify({"logout successfully": current_user}), 200)
        else:
            return make_response(jsonify({"message": "Token already revoked"}), 400)
    
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
            'addresses': [
                    {
                        'country': address.country,
                        'city': address.city,
                        'districts': address.districts,
                        'provinces': address.provinces,
                        'street': address.street,
                        'state': address.state,
                        'zipcode': address.zipcode,
                    } for address in user.addresses
                ] if user.addresses else None
            }
            user_list.append(user_dict)

            return make_response(jsonify({'users': user_list}), 200)

        
class SearchResource(Resource):
    def get(self):
        country = request.args.get('country')
        state = request.args.get('state')
        city = request.args.get('city')
        provinces = request.args.get('provinces')
        districts  = request.args.get('districts')
        street  = request.args.get('street')
        name =  request.args.get('name')


        users_query = User.query.join(Address)

        if country:
            users_query = users_query.filter(Address.country == country)
        if state:
            users_query = users_query.filter(Address.state == state)
        if city:
            users_query = users_query.filter(Address.city == city)
        if provinces:
             users_query = users_query.filter(Address.provinces == provinces)
        if districts:
             users_query = users_query.filter(Address.districts == districts)
        if street:
             users_query = users_query.filter(Address.street == street)
        if name:
             users_query = users_query.filter(User.name == name)

        users = users_query.all()
        if not users:
            return make_response(jsonify({'message': 'No users found!'}), 200)
        user_list = []
        for user in users:
            user_details = {
                "name": user.name,
                "last_name": user.last_name,
                "email": user.email,
                "gender": user.gender,
                "contact": user.contact,
                "services_offered": user.services_offered,
                "addresses": [
                    {
                        "country": address.country,
                        "state": address.state,
                        "city": address.city,
                        "districts": address.districts,
                        "provinces": address.provinces,
                        "street": address.street,
                        "zipcode": address.zipcode
                        }
                        for address in user.addresses
                        ]
                        }
            user_list.append(user_details)
            
        return make_response(jsonify({"users": user_list}), 200)
    
class BookingResource(Resource):
    def post(self):
        data = request.json
        name = data.get("name")
        email = data.get("email")
        services = data.get("services")
        address = data.get("address")
        date = data.get("date")
        users_id = data.get("users_id")

        booking = Booking(name=name, services=services, address=address, date=date, email=email, users_id=users_id)
        db.session.add(booking)
        db.session.commit()

        mechanics = User.query.get(users_id)
        mechanic_email = mechanics.email
        send_booking_car_owner(email)
        send_booking_email(mechanic_email, name, services, address, email, date)
       
        return make_response(jsonify({'message': "Booking successfull"}), 200)

def send_booking_email(mechanic_email, name, services, address, email, date):
    subject = 'New Car Booking'
    body = f"Dear Mechanic,\n\nYou have a new booking from {name} ({mechanic_email}) {services} {address} {email} for {date}.\n\nBest regards,\nYour Car Booking System"
    msg = Message(subject, recipients=[mechanic_email], body=body)
    mail.send(msg)

def send_booking_car_owner(email):
    subject = 'your booking is successful sent'
    body = f"Dear Customer,Best regards, GloMec Your best Car Booking System"
    msg = Message(subject, recipients=[email], body=body)
    mail.send(msg)

