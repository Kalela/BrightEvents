#contains RESTful apis
from flask_api import FlaskAPI
from flask import jsonify, request, session
from flasgger import Swagger, swag_from
from api_data import Users
from api_data import Events
from api_documentation import Documentation

app = FlaskAPI(__name__)
swagger = Swagger(app)
users = Users()
events = Events()
docs = Documentation()

class MyApis(object):
    """Hold all api routes"""
    #Works
    @app.route('/api/v2/auth/register', methods=['POST'])
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
    #{"username":"user" , "password":"123"} for input

    #Works
    @app.route('/api/v2/auth/login', methods=['POST'])
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
    #{"username":"user" , "password":"123"} for input

    #Works
    @app.route('/api/v2/auth/logout', methods=['POST'])
    @swag_from(docs.logout_dict)
    def logout_json():
        """Log out users"""
        user = {}
        if 'username' in session:
            session.pop('username')
            return jsonify("User logged out"), 201
        else:
            return jsonify('User is not logged in'), 200
        #{'username':'kalela'}


    #Works
    @app.route('/api/v2/auth/reset-password', methods=['POST'])
    @swag_from(docs.pass_reset_dict)
    def reset_password_json():
        """Reset users password"""
        if 'username' in session:
            old_user = {}
            old_user[request.form['username']] = request.form['password']
            if old_user in users.users:
                user = {}
                user[session['usernsme']] = request.form['new_password']
                users.users.append(user)
                return jsonify({"Password changed from": old_user},{"To":user}), 201
            else:
                return jsonify("User does not exist"), 404     
        else:
            return jsonify("Please log in"), 401
        #pop old user and password
        
    #Works
    @app.route('/api/v2/events', methods=['POST', 'GET'])
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
            return jsonify({'events':events}), 200

    #Fails
    @app.route('/api/v2/events/<eventid>', methods=['PUT', 'DELETE'])
    def event_update_json(eventid):#check if event exists
        """Edit existing events"""
        if request.method == 'PUT':
            i = 0
            while i < len(events.events):
                try:
                    if events[i][str(eventid)]:
                        old_eventname = events[i][str(eventid)][0]
                        old_date = events[i][str(eventid)][2] 
                        old_location = events[i][str(eventid)][1] 
                        old_category = events[i][str(eventid)][3]
                        old_event = {}
                        old_event = {str(eventid):[old_eventname, old_location, old_date, old_category]}
                        events.events.remove(old_event)
                        
                        eventname = request.form['eventid']
                        date = request.form['date']
                        location = request.form['location']
                        category = request.form['category']
                        updated_event = {}
                        updated_event = {str(eventid):[eventname, location, date, category]}
                        events.events.append(updated_event)
                        i += 1
                        return jsonify({"Edited to":updated_event}), 201
                    else:
                        i += 1
                except (KeyError, ValueError):
                    i += 1
                    pass

        if request.method == 'DELETE':
            i = 0
            while i < len(events.events):
                try:
                    if events[i][str(eventid)]: 
                        eventname = events[i][str(eventid)][0]
                        date = events[i][str(eventid)][2]
                        location = events[i][str(eventid)][1]
                        category = events[i][str(eventid)][3]
                        updated_event = {}
                        target_event = {str(eventid):[eventname, location, date]}
                        print(target_event)
                        i += 1
                        if target_event in events:
                            events.events.pop(target_event)
                            return jsonify({"Events":events.events}), 201
                        else:
                            i += 1
                except (KeyError, ValueError):
                    i += 1
                    pass
            
    #Fails with more than 1 event
    @app.route('/api/v2/events/<eventid>/rsvp', methods=['POST'])
    def rsvp_json(eventid):
        """Send RSVPs to existing events"""
        if 'username' in session:
            evn = [event for event in events.events if event[str(eventid)] == str(eventid)]
            if evn in events.rsvps:
                return jsonify("RSVP already sent"), 409
            else:
                events.rsvps.append(evn)
                return jsonify({"RSVP Sent to":rsvps}), 201
        else:
            return jsonify("Please log in Before sending RSVP"), 401

    if __name__ == '__main__':
        app.run(debug=True)