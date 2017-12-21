#contains RESTful apis
from flask_api import FlaskAPI
from flask import Flask, jsonify, request, session, Blueprint
from flasgger import Swagger, swag_from
from api_data import Users, Events
from api_documentation import Documentation

api = Blueprint('api', __name__)
app = FlaskAPI(__name__)
swagger = Swagger(app)
users = Users()
events = Events()
docs = Documentation()
app.config['SECRET_KEY'] = "mysecret"

class MyApis(object):
    """Hold all api routes"""
    #Works
    @api.route('/auth/register', methods=['POST'])
    @swag_from(docs.register_dict)
    def register_page_json():
        """Add new users to data"""
        if request.method == 'POST':
            user = {}
            user[request.form['username']] = request.form['password']
            if user in users.users:
                return jsonify("User already registered"), 409
            else:
                users.users.append(user)
                return jsonify({'users':users.users}), 201

    #Works
    @api.route('/auth/login', methods=['POST'])
    @swag_from(docs.login_dict)
    def login_json():
        """Login registered users"""
        user = {}
        user[request.form['username']] = request.form['password']
        if user in users.users:
            session['username'] = request.form['username']
            return jsonify("Logged in"), 201
        else:
            return jsonify("Please sign up or review your login info"), 401

    #Works
    @api.route('/auth/logout', methods=['POST'])
    @swag_from(docs.logout_dict)
    def logout_json():
        """Log out users"""
        user = {}
        if 'username' in session:
            session.pop('username')
            return jsonify("User logged out"), 201
        else:
            return jsonify('User is not logged in'), 200

    #Works
    @api.route('/auth/reset-password', methods=['POST'])
    @swag_from(docs.pass_reset_dict)
    def reset_password_json():
        """Reset users password"""
        if 'username' in session:
            old_user = {}
            old_user[request.form['username']] = request.form['password']
            if old_user in users.users:
                user = {}
                user[session['username']] = request.form['new_password']
                users.users.append(user)
                return jsonify({"Password changed from": old_user},{"To":user}), 201
            else:
                return jsonify("User does not exist"), 404     
        else:
            return jsonify("Please log in"), 401
        
    #Works
    @api.route('/events', methods=['POST', 'GET'])
    @swag_from(docs.event_dict)
    def events_json():
        """Add or view events"""
        if request.method == 'POST':
            if 'username' in session:
                location = []
                location = [request.form['eventid'], request.form['location'], request.form['date'], request.form['category']]
                event = {}
                event[request.form['eventid']] = str(location)
                if event in events.events:
                    return jsonify("Event is already added"), 409
                else:
                    events.events.append(event)
                    events.user_events.append(event)
                    return jsonify({'events':events.events}, {"user events":events.user_events}), 201
            else:
                return jsonify("Please Log In to add events"), 401
        if request.method == 'GET':
            return jsonify({'events':events.events}, {"user events": events.user_events}), 200

    #Works
    @api.route('/events/<eventid>', methods=['PUT', 'DELETE'])
    def event_update_json(eventid):
        """Edit existing events"""
        if request.method == 'PUT':
            if 'username' in session:
                i = 0
                while i < len(events.user_events):
                    try:
                        if events.user_events[i][str(eventid)]:
                            old_event ={str(eventid):events.user_events[i][str(eventid)]}
                            if old_event in events.user_events:
                                events.user_events.remove(old_event)
                                events.events.remove(old_event)
                                eventname = request.form['eventid']
                                date = request.form['date']
                                location = request.form['location']
                                category = request.form['category']
                                updated_event = {}
                                updated_event = {str(eventid):[eventname, location, date, category]}
                                events.user_events.append(updated_event)
                                events.events.append(updated_event)
                                i += 1
                                return jsonify({"Edited from: ": old_event}, {"To": updated_event}), 201
                            else:
                                i += 1
                        else:
                            i += 1
                    except (KeyError, ValueError, TypeError):
                        i += 1
                        pass
                    if TypeError:
                        return jsonify("The event you are editing does not exist"), 404
            else:
                return jsonify("Please log in to edit events"), 401

        if request.method == 'DELETE':
            if 'username' in session:
                i = 0
                while i < len(events.user_events):
                    try:
                        if events.user_events[i][str(eventid)]: 
                            target_event = {str(eventid):events.user_events[i][str(eventid)]}
                            i += 1
                            if target_event in events.user_events:
                                events.user_events.remove(target_event)
                                events.events.remove(target_event)
                                return jsonify({"User events":events.user_events}), 201
                    except (KeyError, ValueError, TypeError):
                        i += 1
                        pass
                    if TypeError:
                        return jsonify("The event you are deleting does not exist"), 404
                        
            else:
                return jsonify("Please log in to delete events"), 401
            
    #Works
    @api.route('/events/<eventid>/rsvp', methods=['POST'])
    def rsvp_json(eventid):
        """Send RSVPs to existing events"""
        if 'username' in session:
            i = 0
            while i < len(events.user_events):
                try:
                    if events.user_events[i][str(eventid)]: 
                        rsvp_event = {str(eventid):events.user_events[i][str(eventid)]}
                        i += 1
                        if rsvp_event in events.user_events:
                            if rsvp_event in events.rsvps :
                                return jsonify("Event already RSVPd")
                            else:
                                events.rsvps.append(rsvp_event)
                                return jsonify({"RSVPs sent":events.rsvps}), 201
                        else:
                            i += 1
                except (KeyError, ValueError, TypeError):
                    i += 1
                    pass
                if TypeError:
                    return jsonify("The event does not exist"), 404
        else:
            return jsonify("Please log in Before sending RSVP"), 401

    app.register_blueprint(api, url_prefix='/api/v2')
    if __name__ == '__main__':
        app.run(debug=True)
