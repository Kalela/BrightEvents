import uuid
import jwt
import datetime
from flask_api import FlaskAPI
from flask import jsonify, request, session, Blueprint, make_response
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger, swag_from
from api_documentation import Documentation
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

from instance.config import app_config

docs = Documentation()
db = SQLAlchemy()

def create_app(config_name):
    """Create the api flask app"""
    from models import User, Event
    
    api = Blueprint('api', __name__)
    app = FlaskAPI(__name__, instance_relative_config=True)
    swagger = Swagger(app)
    
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
    
    def print_events(events):
        result = []
        for event in events:
            event_data = {}
            event_data['eventname'] = event.eventname
            event_data['location'] = event.location
            event_data['date'] = event.date
            event_data['category'] = event.category
            result.append(event_data)
        return result

    @api.route('/auth/register', methods=['POST'])
#    @swag_from(docs.register_dict)
    def register_page_json():
        """Add new users to data"""
        if request.method == 'POST':
                username = request.form['username']
                email = request.form['email']
                password = request.form['password']
                hashed_password = generate_password_hash(request.form['password'], method='sha256')

                if username and email and hashed_password:
                    user = User.query.filter_by(username=username).first()
                    if not user:
                        user = User(username=username, email=email, password=hashed_password, public_id=str(uuid.uuid4()), logged_in = False)
                        user.save()
                        return jsonify({'id':user.public_id,
                                        'logged in':user.logged_in,
                                        'username':user.username,
                                        'password':user.password,
                                        'email':user.email,
                                        'date_created': user.date_created,
                                        'date_modified': user.date_modified}), 201
                    else:
                        return jsonify("Username or email already registered"), 409
                else:
                    return jsonify({"message":"Please insert missing value(s)"}), 409

    @api.route('/auth/login', methods=['POST'])
#    @swag_from(docs.login_dict)
    def login_json():
        """Login registered users"""
        name = request.form['username']
        passwd = request.form['password']
        
        if not name or not passwd:
            return make_response('Could not verify', 401, {'WWW-Authenticate':'Basic realm="Login required!"'})
        
        user = User.query.filter_by(username=name).first()
        if not user:
            return make_response('Could not verify', 401, {'WWW-Authenticate':'Basic realm="Login required!"'})
        
        if check_password_hash(user.password, passwd):
            token = jwt.encode({'public_id':user.public_id, 'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, app.config['SECRET_KEY'])
            user.logged_in = True
            db.session.commit()
            return jsonify({'Logged in':user.username, 'access-token':token.decode('UTF-8')}), 202
        
        return make_response('Could not verify', 401, {'WWW-Authenticate':'Basic realm="Login required!"'})

    @api.route('/auth/logout', methods=['POST'])
    @token_required
#    @swag_from(docs.logout_dict)
    def logout_json(current_user):
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
#    @swag_from(docs.pass_reset_dict)
    def reset_password_json(current_user):
        """Reset users password"""
        user = current_user
        old_password = user.password
        new_password = generate_password_hash(request.form['new_password'], method='sha256')

        if user.logged_in == True:
                user.password = new_password
                db.session.commit()
                return jsonify({"Message":"Password reset!"}), 205 
        else:
            return jsonify({"message":"Please log in"}), 401

    @api.route('/events', methods=['POST', 'GET'])
    @token_required
#    @swag_from(docs.event_get_dict, methods=['GET'])
#    @swag_from(docs.event_post_dict, methods=['POST'])
    def events_json(current_user):
        """Add or view events"""
        user = current_user
        if request.method == 'POST':
            if user.logged_in == True:
                eventname = request.form['eventname']
                location = request.form['location']
                date = request.form['date']
                category = request.form['category']
                if eventname and location and date and category:
                    try:
                        event = Event.query.filter_by(eventname=eventname).first()
                        if event and event.location == location:
                            return jsonify({"message":"Event already exists"}), 409
                        else:
                            event = Event(eventname=eventname, location=location, date=date, category=category, rsvp="None")
                            event.save()
                            return jsonify({"New event":
                                           {"id":event.id,
                                            "eventname":event.eventname,
                                            "location":event.location,
                                            "date":event.date,
                                            "category":event.category,
                                            'date_created': event.date_created,
                                            'date_modified': event.date_modified
                                            }}), 201
                    except:
                        return jsonify({"message":"Something went wrong(Common cause: Bad date input)"}), 400
                     
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
            _next = False
            prev = False
            
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
#    @swag_from(docs.event_put_dict, methods=['PUT'])
#    @swag_from(docs.event_delete_dict, methods=['DELETE'])
    def event_update_json(current_user, eventname):
        """Edit existing events"""
        user = current_user
        if user.logged_in == True:
            if request.method == 'PUT':
                event_name = request.form['eventid']
                date = request.form['date']
                location = request.form['location']
                category = request.form['category']
                event = Event.get_one(eventname)
                try:
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
                except:
                    return jsonify({"message":"Something went wrong(Common cause: Bad date input)"}), 400

            if request.method == 'DELETE':
                event = Event.get_one(eventname)
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
#    @swag_from(docs.event_rsvp_dict)
    def rsvp_json(current_user, eventname):
        """Send RSVPs to existing events"""
        user = current_user
        if user.logged_in == True:
            event = Event.get_one(eventname)
            if event:
                if event.rsvp == "None":
                    event.rsvp = "Sent"
                    db.session.commit()
                    return jsonify({"message":"RSVP sent"}), 201
                else:
                    return jsonify({"message":"RSVP already sent"}), 409
            else:
                return jsonify({"message":"Event does not exist"}), 404
        else:
            return jsonify({"message":"Please log in Before sending RSVP"}), 401

    app.register_blueprint(api, url_prefix='/api/v2')
    return app

