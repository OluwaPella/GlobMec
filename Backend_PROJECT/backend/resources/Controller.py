from models import User, Address, db, Booking
from flask import request, make_response, jsonify
from flask_restful import Resource
from flask_mail import Message, Mail
from flask_jwt_extended import JWTManager, create_access_token
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
jwt = JWTManager()
mail = Mail()

class RegisterResource(Resource):
    def post(self):
        data = request.json


        existing_user = User.query.filter(User.email == data.get('email')) and User.query.filter(User.contact == data.get('contact')).first()
        if existing_user:
            return jsonify({"message": "User  or contacts already exists"})

        password = data.get('password')
        if not all([data.get('name'), data.get('lastname'), data.get('email'), password, data.get('gender'), data.get('contact'), data.get('country'), data.get('services')]):
            return jsonify({'message': 'Incomplete details'})
        elif any(c.isalpha() for c in password) and any(c.isdigit() for c in password): 
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        else:
            return jsonify({'message': 'Password must contain at least one letter and one number'})

        new_user = User(
                name=data.get('name'),
                lastname=data.get('lastname'),
                email=data.get('email'),
                password=hashed_password,
                gender=data.get('gender'),
                contact=data.get('contact'),
                services=data.get('services')
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
        
        return jsonify({'message': 'Register successful'})

class LoginResource(Resource):
    def post(self):
        data = request.json
        email = data.get("email")
        password = data.get("password")
        
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.name)
            return make_response(jsonify({
                "Successful login": {
                    "access_token" : access_token,
                    'name' : user.name,
                    'email' : user.email
                    }
            }), 200)
        return jsonify({"error": "Invalid email or password"})
      

class UsersResource(Resource):
    def get(self):
        users = User.query.all()

        user_list = []

        for user in users:
            user_dict = {
            'id': user.id,
            'name': user.name,
            'lastname': user.lastname,
            'email': user.email,
            'gender': user.gender,
            'contact': user.contact,
            'services': user.services,
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

            return jsonify({'users': user_list})

        
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
            return jsonify({'message': 'No users found!'})
        user_list = []
        for user in users:
            user_details = {
                "name": user.name,
                "lastname": user.lastname,
                "email": user.email,
                "gender": user.gender,
                "contact": user.contact,
                "services": user.services,
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
            
        return jsonify({"users": user_list})
    
class BookingResource(Resource):
    def post(self, user_id):
        data = request.json
        name = data.get("name")
        email = data.get("email")
        services = data.get("services")
        address = data.get("address")
        date = data.get("date")

        booking = Booking(name=name, services=services, address=address, date=date, email=email, user_id=user_id)
        db.session.add(booking)
        db.session.commit()

        mechanics = User.query.get(user_id)
        mechanic_email = mechanics.email
        send_booking_car_owner(email)
        send_booking_email(mechanic_email, name, services, address, email, date)
       
        return jsonify({'message': "Booking successfull"})

"""def send_booking_email(mechanic_email, name, services, address, email, date):
    subject = 'New Car Booking'
    body = f"Dear Mechanic,\n\nYou have a new booking from {name} ({mechanic_email}) {services} {address} {email} for {date}.\n\nBest regards,\nYour Car Booking System"
    msg = Message(subject, recipients=[mechanic_email], body=body)
    mail.send(msg)

def send_booking_car_owner(email):
    subject = 'your booking is successful sent'
    body = f"Dear Customer,Best regards, GloMec Your best Car Booking System"
    msg = Message(subject, recipients=[email], body=body)
    mail.send(msg)
"""

