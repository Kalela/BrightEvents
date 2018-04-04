#import dependancies
import uuid
from flask import request

from werkzeug.security import generate_password_hash, check_password_hash

from webapi.helper_functions import check_registration_input, check_password_reset

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

def reset_password_helper(current_user, db):
    status_code = 500
    statement = {}
    new_password = request.data['new_password'].strip()
    confirm_password = request.data['confirm_password'].strip()
    if check_password_reset(new_password, confirm_password, current_user, status_code)[0]:
        status_code = check_password_reset(new_password,
                                           confirm_password,
                                           current_user, status_code)[1]
        statement = check_password_reset(new_password,
                                         confirm_password,
                                         current_user, status_code)[0]
    else:
        if current_user and current_user.logged_in is True:
            current_user.password = check_password_reset(new_password,
                                                 confirm_password,
                                                 current_user, status_code)[2]
            db.session.commit()
            status_code = 205
            statement = {"Message":"Password reset!"}
        else:
            status_code = 401
            statement = {"message":"Please log in"}
    return statement, status_code
