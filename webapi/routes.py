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
                user.password == new_password
                user.save()
                return jsonify({"Password changed from": old_password},{"To":new_password}), 205
            else:
                return jsonify("Wrong password input. Review your input."), 400  
        else:
            return jsonify("Please log in"), 401
#        
#    #Works
#    @api.route('/events', methods=['POST', 'GET'])
#    @swag_from(docs.event_get_dict, methods=['GET'])
#    @swag_from(docs.event_post_dict, methods=['POST'])
#    def events_json():
#        """Add or view events"""
#        if request.method == 'POST':
#            if 'username' in session:
#                location = []
#                location = [request.form['eventid'], request.form['location'], request.form['date'], request.form['category']]
#                event = {}
#                event[request.form['eventid']] = str(location)
#                if event in events.events:
#                    return jsonify("Event is already added"), 409
#                else:
#                    events.events.append(event)
#                    events.user_events.append(event)
#                    return jsonify({'events':events.events}, {"user events":events.user_events}), 201
#            else:
#                return jsonify("Please Log In to add events"), 401
#        if request.method == 'GET':
#            return jsonify({'events':events.events}, {"user events": events.user_events}), 200
#
#    #Works
#    @api.route('/events/<eventid>', methods=['PUT', 'DELETE'])
#    @swag_from(docs.event_put_dict, methods=['PUT'])
#    @swag_from(docs.event_delete_dict, methods=['DELETE'])
#    def event_update_json(eventid):
#        """Edit existing events"""
#        if 'username' in session:
#            if request.method == 'PUT':
#
#                    i = 0
#                    status_code = 0
#                    while i < len(events.user_events):
#                        try:
#                            if events.user_events[i][str(eventid)]:
#                                old_event ={str(eventid):events.user_events[i][str(eventid)]}
#                                if old_event in events.user_events:
#                                    eventname = request.form['eventid']
#                                    date = request.form['date']
#                                    location = request.form['location']
#                                    category = request.form['category']
#                                    updated_event = {}
#                                    updated_event = {str(eventid):[eventname, location, date, category]}
#                                    events.user_events.append(updated_event)
#                                    events.events.append(updated_event)         
#                                    status_code = 202
#                                    events.user_events.remove(old_event)
#                                    events.events.remove(old_event)
#                                    return jsonify({"Event edited to: ": updated_event}), 202
#
#                        except (KeyError, ValueError, TypeError):
#                            if TypeError:
#                                i += 1
#                        if i >= len(events.user_events):
#                            if status_code != 202:
#                                return jsonify("The event you are editing does not exist"), 404
#            if request.method == 'DELETE':
#                    i = 0
#                    status_code = 0
#                    while i < len(events.user_events):
#                        try:
#                            if events.user_events[i][str(eventid)]:
#                                target_event = {str(eventid):events.user_events[i][str(eventid)]}
#                                status_code = 205
#                                i += 1
#
#                        except (KeyError, ValueError, TypeError):
#                            if TypeError:
#                                i += 1
#                        if i >= len(events.user_events):
#                                    if status_code != 205:
#                                        return jsonify("The event you are deleting does not exist"), 404
#                                    else:
#                                        events.user_events.remove(target_event)
#                                        return jsonify({"User events":events.user_events}), 205
#                    
#        else:
#            return jsonify("Please log in to edit or delete events"), 401
#            
#    #Works
#    @api.route('/events/<eventid>/rsvp', methods=['POST'])
#    @swag_from(docs.event_rsvp_dict)
#    def rsvp_json(eventid):
#        """Send RSVPs to existing events"""
#        if 'username' in session:
#            i = 0
#            while i < len(events.user_events):
#                try:
#                    if events.user_events[i][str(eventid)]: 
#                        rsvp_event = {str(eventid):events.user_events[i][str(eventid)]}
#                        if rsvp_event in events.user_events:
#                            if rsvp_event in events.rsvps :
#                                status_code = 409
#                                return jsonify("Event already RSVPd"), 409
#                            else:
#                                events.rsvps.append(rsvp_event)
#                                status_code = 201
#                                return jsonify({"RSVPs sent":events.rsvps}), 201
#                        else:
#                            i += 1
#                except (KeyError, ValueError, TypeError):
#                    if TypeError:
#                        i += 1
#                if i >= len(events.user_events):
#                    if status_code != 201 and status_code != 409:
#                        return jsonify("The event does not exist"), 404
#        else:
#            return jsonify("Please log in Before sending RSVP"), 401
    

    app.register_blueprint(api, url_prefix='/api/v2')
    return app

