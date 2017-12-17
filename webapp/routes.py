#contains RESTful apis
from flask import jsonify, request, session
from app import app
from flasgger import Swagger, swag_from

swagger = Swagger(app)

users = [{'kalela':'Kalela'}, {'khal':'khal'}, {'user':'password'}, {'admin':'admin'}]
events = [{"MyParty": "['Myparty','Nairobi', '12/25/2017', 'Party']"}]
user_events = []
rsvps = []

class MyApis(object):
    """Hold all api routes"""
    #Works
    @app.route('/api/v2/auth/register', methods=['POST'])
    @swag_from('swagger.yaml')
    def register_page_json():
        """Add new users to data"""
        if request.method == 'POST':
            user = {}
            user[request.json['username']] = request.json['password']
            if user in users:
                return jsonify("User already registered"), 201
            else:
                users.append(user)
                return jsonify({'users':users}), 201
    #{"username":"user" , "password":"123"} for input

    #Works
    @app.route('/api/v2/auth/login', methods=['POST'])
    def login_json():
        """Login registered users"""
        user = {}
        user[request.json['username']] = request.json['password']
        if user in users:
            session['username'] = request.json['username']
            return jsonify("Logged in"), 201
        else:
            return jsonify("Please sign up or review your login info"), 201
    #{"username":"user" , "password":"123"} for input

    #Works
    @app.route('/api/v2/auth/logout', methods=['POST'])
    def logout_json():
        """Log out users"""
        user = {}
        if 'username' in session:
            session.pop('username')
            return jsonify("User logged out"), 201
        else:
            return jsonify('User is not logged in'), 201
        #{'username':'kalela'}


    #Works  ??
    @app.route('/api/v2/auth/reset-password', methods=['POST'])
    def reset_password_json():
        """Reset users password"""
        if 'username' in session:
            user = {}
            user[session['username']] = request.json['new_password']
            users.append(user)
            return jsonify("Password changed"), 201
        else:
            return jsonify("Please log in"), 201
        #pop old user and password
        
    #Works
    @app.route('/api/v2/events', methods=['POST', 'GET'])
    def events_json():
        """Add or view events"""
        if request.method == 'POST':
            if 'username' in session:
                location = []
                location = [request.json['eventid'], request.json['location'], request.json['date'], request.json['category']]
                event = {}
                event[request.json['eventid']] = str(location)

                if event in events:
                    return jsonify("Event is already added"), 201
                else:
                    events.append(event)
                    user_events.append(event)
                    return jsonify({'events':events}, {"user events":user_events}), 201
            else:
                return jsonify("Please Log In to add events"), 201
        if request.method == 'GET':
            return jsonify({'events':events}), 200

    #Fails
    @app.route('/api/v2/events/<eventid>', methods=['PUT', 'DELETE'])
    def event_update_json(eventid):#check if event exists
        """Edit existing events"""
        if request.method == 'PUT':
            i = 0
            while i < len(events):
                try:
                    if events[i][str(eventid)]:
                        old_eventname = events[i][str(eventid)][0]
                        old_date = events[i][str(eventid)][2] 
                        old_location = events[i][str(eventid)][1] 
                        old_category = events[i][str(eventid)][3]
                        old_event = {}
                        old_event = {str(eventid):[old_eventname, old_location, old_date, old_category]}
                        events.remove(old_event)
                        print (events)
                        
                        eventname = request.json['eventid']
                        date = request.json['date']
                        location = request.json['location']
                        category = request.json['category']
                        updated_event = {}
                        updated_event = {str(eventid):[eventname, location, date, category]}
                        events.append(updated_event)
                        print(updated_event)
                        i += 1
                        return jsonify({"Edited to":updated_event}), 201
                except (KeyError, ValueError):
                    i += 1
                    pass

        if request.method == 'DELETE':
            i = 0
            while i < len(events):
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
                            events.pop(target_event)
                            return jsonify({"Events":events}), 201
                except (KeyError, ValueError):
                    i += 1
                    pass
            
    #Fails with more than 1 event
    @app.route('/api/v2/events/<eventid>/rsvp', methods=['POST'])
    def rsvp_json(eventid):
        """Send RSVPs to existing events"""
        if 'username' in session:
            evn = [event for event in events if event[str(eventid)] == str(eventid)]
            if evn in rsvps:
                return jsonify("RSVP already sent"), 201
            else:
                rsvps.append(evn)
                return jsonify({"RSVP Sent to":rsvps}), 201
        else:
            return jsonify("Please log in Before sending RSVP"), 201

    if __name__ == '__main__':
        app.run(debug=True)
