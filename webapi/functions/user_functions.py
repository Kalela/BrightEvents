#import dependancies
import uuid
import passwordmeter
import datetime
import jwt
from flask import request

from werkzeug.security import generate_password_hash, check_password_hash

from webapi.helper_functions import check_registration_input, check_password_reset

meter = passwordmeter.Meter(settings=dict(factors='length'))

def register_helper(User):
    status_code = 500
    statement = {}
    username = request.data['username'].strip()
    email = request.data['email'].strip()
    password = request.data['password'].strip()
    if check_registration_input(username, email, password):
        status_code = 400
        statement = (check_registration_input(username, email, password))
    else:
        password_strength, improvements = meter.test(password)
        if password_strength < 0.5:
            status_code = 400
            statement = {"message":"At least 6 characters required for password"}
        else:
            hashed_password = generate_password_hash(request.data['password'], method='sha256')
            user = User.query.filter_by(username=username).first()
            if not user:
                user = User(username=username, email=email,
                            password=hashed_password, public_id=str(uuid.uuid4()),
                            logged_in=False)
                user.save()
                status_code = 201
                statement = {"message":"Registration successful, log in to access your account"}
            else:
                status_code = 409
                statement = {"message":"Username or email already registered"}
    return statement, status_code

def login_helper(User, app, db):
    status_code = 500
    statement = {}
    name = request.data['username'].strip()
    passwd = request.data['password'].strip()

    if not name or not passwd:
        statement = {"message":"Name or password missing!"}
        status_code = 400
    else:
        user = User.query.filter_by(username=name).first()
        if not user:
            statement = {"message":"Please log in to a registered account"}
            status_code = 401
        elif check_password_hash(user.password, passwd):
            token = jwt.encode({'public_id':user.public_id,
                                'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=4320)}, app.config['SECRET_KEY'])
            user.logged_in = True
            db.session.commit()
            statement = {'Logged_in':user.username,
                            'access_token':token.decode('UTF-8')}
            status_code = 202
        elif not check_password_hash(user.password, passwd):
            statement = {"message":"Wrong password! Please check your input."}
            status_code = 401
    return statement, status_code

def logout_helper(current_user, db):
    status_code = 500
    statement = {}
    if current_user and current_user.logged_in is True:
        current_user.logged_in = False
        db.session.commit()
        status_code = 202
        statement = {"message":"User logged out"}
    else:
        status_code = 200
        statement = {"message":"User is already logged out"}
    return statement, status_code

def confirm_account_helper(email, db):
    """Helper function for confirming a user's email is real"""
    user = User.query.filter_by(email=email).first()
    user.email_confirmed = True
    db.session.commit()
    return {"message":"Email confirmed"}, 200

def reset_password_helper(email, User, db):
    new_password = request.data["password"]
    hashed_password = generate_password_hash(new_password, method='sha256')
    user = User.query.filter_by(email=email).first()
    if user:
        user.password = hashed_password
        db.session.commit()
        statement = {"message":"Password reset! Please use your new password to log in"}
    return statement, 201
