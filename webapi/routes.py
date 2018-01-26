from flask_api import FlaskAPI
from flask import jsonify, request, session, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger, swag_from
from api_documentation import Documentation

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

    #Works
    @api.route('/auth/register', methods=['POST'])
#    @swag_from(docs.register_dict)
    def register_page_json():
        """Add new users to data"""
        if request.method == 'POST':
                username = request.form['username']
                email = request.form['email']
                password = request.form['password']

                if username and email and password:
                    try:
                        user = User(username=username, email=email, password=password)
                        user.save()
                        return jsonify({'id':user.id,
                                        'username':user.username,
                                        'password':user.password,
                                        'email':user.email,
                                        'date_created': user.date_created,
                                        'date_modified': user.date_modified}), 201
                    except:
                        return jsonify("Username or email already registered"), 409   
                else:
                    return jsonify("Please insert missing value(s)"), 409

    #Works
    @api.route('/auth/login', methods=['POST'])
#    @swag_from(docs.login_dict)
    def login_json():
        """Login registered users"""
        if 'username' in session:
            return jsonify("User", session['username'], "already logged in."), 409
        else:
            username = request.form['username']
            password = request.form['password']
            user = User.get_one(username)

            if username and password:
                if user.username == username and user.password == password:
                    results = user.username
                    session['username'] = user.username
                    return jsonify({"Logged in as": results}), 202
                else:
                    return jsonify("The Password and Username combination is not correct"), 401

    #Works
    @api.route('/auth/logout', methods=['POST'])
#    @swag_from(docs.logout_dict)
    def logout_json():
        """Log out users"""
        if 'username' in session:
            session.pop('username')
            return jsonify("User logged out"), 202
        else:
            return jsonify('User is not logged in'), 200

    #Works
    @api.route('/auth/reset-password', methods=['POST'])
    @swag_from(docs.pass_reset_dict)
    def reset_password_json():
        """Reset users password"""
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        
        if 'username' in session:
            user = User.get_one(session['username'])
            if user.password == old_password:
                user.password = new_password
                db.session.commit()
                return jsonify({"Password changed from": old_password},{"To":new_password}), 205
            else:
                return jsonify("Wrong password input. Review your input."), 400  
        else:
            return jsonify("Please log in"), 401
        
    #Works
    @api.route('/events', methods=['POST', 'GET'])
#    @swag_from(docs.event_get_dict, methods=['GET'])
#    @swag_from(docs.event_post_dict, methods=['POST'])
    def events_json():
        """Add or view events"""
        if request.method == 'POST':
            if 'username' in session:
                eventname = request.form['eventname']
                location = request.form['location']
                date = request.form['date']
                category = request.form['category']
                if eventname and location and date and category:
                    try:
                        event = Event(eventname=eventname, location=location, date=date, category=category, rsvp="None")
                        event.save()
                        return jsonify("New event",
                                       {"id":event.id,
                                        "eventname":event.eventname,
                                        "location":event.location,
                                        "date":event.date,
                                        "category":event.category,
                                        'date_created': event.date_created,
                                        'date_modified': event.date_modified
                                        }), 201
                    except:
                        return jsonify("Event already exists"), 409 
            else:
                return jsonify("Please Log In to add events"), 401
        if request.method == 'GET':
            events = Event.get_all()
            return jsonify("Events", str(events)), 200

    #Works
    @api.route('/events/<eventname>', methods=['PUT', 'DELETE'])
#    @swag_from(docs.event_put_dict, methods=['PUT'])
#    @swag_from(docs.event_delete_dict, methods=['DELETE'])
    def event_update_json(eventname):
        """Edit existing events"""
        if 'username' in session:
            if request.method == 'PUT':
                event_name = request.form['eventid']
                date = request.form['date']
                location = request.form['location']
                category = request.form['category']
                try:
                    event = Event.get_one(eventname)
                    event.eventname = event_name
                    event.location = location
                    event.date = date
                    event.category = category
                    db.session.commit()
                    return jsonify({"Event updated to: ":{
                                    "eventname":event_name,
                                    "location":location,
                                    "date":date,
                                    "category":category
                                   }}), 202
                except:
                    return jsonify("Event you are editing does not exist"), 404

            if request.method == 'DELETE':
                try:
                    event = Event.get_one(eventname)
                    event.delete()
                    events = Event.get_all()
                    return jsonify("Event(s)", str(Event.get_all())), 205
                except:
                    return jsonify("Event you are deleting does not exist"), 404
                    
        else:
            return jsonify("Please log in to edit or delete events"), 401
            
    #Works
    @api.route('/events/<eventname>/rsvp', methods=['POST'])
    @swag_from(docs.event_rsvp_dict)
    def rsvp_json(eventname):
        """Send RSVPs to existing events"""
        if 'username' in session:
            try:
                event = Event.get_one(eventname)
                if event.rsvp == "None":
                    event.rsvp = "Sent"
                    db.session.commit()
                    return jsonify("RSVP sent"), 201
                else:
                    return jsonify("RSVP already sent"), 409
            except:
                return jsonify("Event does not exist"), 404
        else:
            return jsonify("Please log in Before sending RSVP"), 401

    app.register_blueprint(api, url_prefix='/api/v2')
    return app

