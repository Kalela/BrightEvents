#Import dependencies
import uuid
import jwt
import time
import datetime
import re

from flask_api import FlaskAPI
from flask import jsonify, request, session, Blueprint, make_response
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger, swag_from
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

from api_documentation import Documentation
from instance.config import app_config

db = SQLAlchemy()

def create_app(config_name):
    """Create the api flask app"""
    from models import User, Event, Rsvp
    from helper_functions import print_events, Category
    
    api = Blueprint('api', __name__)
    app = FlaskAPI(__name__, instance_relative_config=True)
    docs = Documentation()
    catgory = Category()
    swagger = Swagger(app,
    template={
        "swagger": "2.0",
        "info": {
            "title": "Bright Events API Documentation",
            "version": "1.0",
    }   
    })
    
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)
    with app.app_context():
        db.create_all()
        
    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None

            if 'x-access-token' in request.headers:
                token = request.headers['x-access-token']    

            if not token:
                return jsonify({"message":"Token is missing!"}), 401

            try:
                data = jwt.decode(token, app.config['SECRET_KEY'])
                current_user = User.query.filter_by(public_id=data['public_id']).first()
            except:
                return jsonify({"message":"Token is invalid"}), 401
            return f(current_user, *args, **kwargs)

        return decorated

    @api.route('/auth/register', methods=['POST'])
    @swag_from(docs.register_dict, methods=['POST'])
    def register():
        """Add new users to data"""
        if request.method == 'POST':
                username = request.form['username'].strip()
                email = request.form['email'].strip()
                password = request.form['password'].strip()

                if not email:
                    return jsonify("Please insert email"), 400
                if "@" not in str(email) or ".com" not in str(email):
                    return jsonify("Please insert a valid email"), 400
                if not username:
                    return jsonify("Please insert username"), 400
                if not password:
                    return jsonify("Please insert password"), 400
                    
                hashed_password = generate_password_hash(request.form['password'], method='sha256')

                if username and email and hashed_password:
                    user = User.query.filter_by(username=username).first()
                    if not user:
                        user = User(username=username, email=email, password=hashed_password, public_id=str(uuid.uuid4()), logged_in = False)
                        user.save()
                        return jsonify({"message":"Registration successful, log in to access your account"}), 201
                    else:
                        return jsonify("Username or email already registered"), 409
                else:
                    return jsonify({"message":"Please insert missing value(s)"}), 409

    @api.route('/auth/login', methods=['POST'])
    @swag_from(docs.login_dict, methods=['POST'])
    def login():
        """Login registered users"""
        name = request.form['username'].strip()
        passwd = request.form['password'].strip()
        
        if not name or not passwd:
            return make_response('Could not verify', 401, {'WWW-Authenticate':'Basic realm="Login required!"'})
        
        user = User.query.filter_by(username=name).first()
        if not user:
            return make_response('Could not verify', 401, {'WWW-Authenticate':'Basic realm="Login required!"'})
        
        if check_password_hash(user.password, passwd):
            token = jwt.encode({'public_id':user.public_id, 'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=9999)}, app.config['SECRET_KEY'])
            user.logged_in = True
            db.session.commit()
            return jsonify({'Logged in':user.username, 'access-token':token.decode('UTF-8')}), 202
        
        return make_response('Could not verify', 401, {'WWW-Authenticate':'Basic realm="Login required!"'})

    @api.route('/auth/logout', methods=['POST'])
    @token_required
    @swag_from(docs.logout_dict, methods=['POST'])
    def logout(current_user):
        """Log out users"""
        user = current_user
        if user.logged_in == True:
            user.logged_in = False
            db.session.commit()
            return jsonify({"message":"User logged out"}), 202
        else:
            return jsonify({"message":"User is already logged out"}), 200

    @api.route('/auth/reset-password', methods=['POST'])
    @token_required
    @swag_from(docs.pass_reset_dict, methods=['POST'])
    def reset_password(current_user):
        """Reset users password"""
        user = current_user
        new_password = request.form['new_password'].strip()
        confirm_password = request.form['confirm_password'].strip()
        if not new_password or not confirm_password:
            return jsonify({"message":"Please insert required fields"}), 400
        if check_password_hash(user.password, new_password):
            return jsonify({"message":"Password already set"}), 409
        if new_password == confirm_password:
            new_password = generate_password_hash(request.form['new_password'], method='sha256')
        else:
            return jsonify({"message":"Passwords don't match"}), 409

        if user.logged_in == True:
                user.password = new_password
                db.session.commit()
                return jsonify({"Message":"Password reset!"}), 205 
        else:
            return jsonify({"message":"Please log in"}), 401

    @api.route('/events', methods=['POST', 'GET'])
    @token_required
    @swag_from(docs.event_post_dict, methods=['POST'])
    @swag_from(docs.event_get_dict, methods=['GET'])
    def events(current_user):
        """Add or view events"""
        user = current_user
        if user.logged_in == True:
            if request.method == 'POST':
                eventname = request.form['eventname'].strip()
                location = request.form['location'].strip()
                date = request.form['date'].strip()
                owner = user.username
                try:
                    date_object = datetime.datetime.strptime(str(date), '%Y/%m/%d')
                except ValueError:
                    return jsonify({"message":"Wrong date format input(Correct:yy/mm/dd)"}), 400
                category = request.form['category'].strip()
                if catgory.category_check(category) == "OK":
                    pass
                else:
                    return jsonify({"message":"Please select a viable category"},
                                  {"options": catgory.category_list}), 406
                if eventname and location and date and category:
                    event = Event.get_one(eventname, owner)
                    if event and event.location == location:
                        event_date = datetime.datetime.strptime(str(event.date), '%Y-%m-%d %H:%M:%S+03:00')
                        if event_date == date_object:
                            return jsonify({"message":"Event already exists"}), 409
                        else:
                            event = Event(event_owner=current_user, eventname=eventname, location=location, date=date, category=category, owner=owner)
                            event.save()
                            return jsonify({"message":"Event has been created"},
                                           {"caution!":"Event with same name and location exists"}), 201

                    else:
                        event = Event(event_owner=current_user, eventname=eventname, location=location, date=date, category=category, owner=owner)
                        event.save()
                        return jsonify({"New event":
                                       {"id":event.id,
                                        "eventname":event.eventname,
                                        "location":event.location,
                                        "date":event.date,
                                        "category":event.category,
                                        "owner":event.owner,
                                        "'date_created": event.date_created,
                                        "date_modified": event.date_modified
                                        }}), 201
                else:
                    return jsonify({"message":"Please insert valid event"}), 400
        else:
            return jsonify({"message":"Please Log In to add events"}), 401

        if request.method == 'GET':
            location = request.args.get('location')
            category = request.args.get('category')
            q = request.args.get('q')
            
            limit = request.args.get('limit')
            if limit:
                limit = int(limit)

            _next = request.args.get('next')
            prev = request.args.get('prev')
            
            if category:
                events = Event.filter_category(category)
            if location:
                events = Event.filter_location(location)
            if q:
                events = Event.query.filter(Event.eventname.ilike('%{}%'.format(q))).all()
            if not category and not location and not q:
                if not limit:
                    limit = 10
                event_pages = Event.get_all_pages(limit)
                events = event_pages.items
            return jsonify({"Events": print_events(events)}), 200

    @api.route('/events/<eventname>', methods=['PUT', 'DELETE'])
    @token_required
    @swag_from(docs.event_put_dict, methods=['PUT'])
    @swag_from(docs.event_delete_dict, methods=['DELETE'])
    def event_update(current_user, eventname):
        """Edit existing events"""
        user = current_user
        if user.logged_in == True:
            if request.method == 'PUT':
                event_name = request.form['event_name'].strip()
                date = request.form['date'].strip()
                try:
                    date_object = datetime.datetime.strptime(str(date), '%Y/%m/%d')
                except ValueError:
                    return jsonify({"message":"Wrong date format input(Correct:yy/mm/dd)"}), 400
                location = request.form['location'].strip()
                category = request.form['category'].strip()
                if catgory.category_check(category) == "OK":
                    pass
                else:
                    return jsonify({"message":"Please select a viable category"},
                                  {"options": catgory.category_list}), 406
                event = Event.get_one(eventname, user.username)
                if event:
                    event.eventname = event_name
                    event.location = location
                    event.date = date
                    event.category = category
                    db.session.commit()
                    return jsonify({"Event updated to:":{
                                "eventname":event_name,
                                "location":location,
                                "date":date,
                                "category":category
                               }}), 202
                else:
                    return jsonify({"message":"Event you are editing does not exist"}), 404

            if request.method == 'DELETE':
                event = Event.get_one(eventname, user.username)
                if event:
                    event.delete()
                    event_pages = Event.get_all_pages(limit=10)
                    events = event_pages.items
                    return jsonify({"Event(s)": print_events(events)}), 205
                else:
                    return jsonify({"message":"Event you are deleting does not exist"}), 404
                    
        else:
            return jsonify({"message":"Please log in to edit or delete events"}), 401

    @api.route('/events/<eventname>/rsvp', methods=['POST'])
    @token_required
    @swag_from(docs.event_rsvp_dict, methods=['POST'])
    def rsvps(current_user, eventname):
        """Send RSVPs to existing events"""
        user = current_user
        if user.logged_in == True:
            event = Event.get_one(eventname, user.username)
            if event:
                rsvp = Rsvp.query.filter_by(owner_id=user.id).all()
                if rsvp:
                    return jsonify({"message":"RSVP already sent"}), 409   
                else:
                    rsvp = Rsvp(rsvp_event=event, event_owner=current_user)
                    rsvp.save()
                    return jsonify({"message":"RSVP sent"}), 201
            else:
                return jsonify({"message":"Event does not exist"}), 404
        else:
            return jsonify({"message":"Please log in Before sending RSVP"}), 401

    app.register_blueprint(api, url_prefix='/api/v2')
    return app

