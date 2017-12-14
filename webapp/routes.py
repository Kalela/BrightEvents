#contains RESTful apis
from flask import jsonify, request, session
from app import app


users = [{'kalela':'Kalela'}, {'khal':'khal'}, {'user':'password'}, {'admin':'admin'}]
events = []
user_events = []
rsvps = []

class MyApis(object):
    """Hold all api routes"""
    #Works
    @app.route('/api/v2/auth/register', methods=['POST'])
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
        if 'username' in session:
            """Reset users password"""
            user = {}
            user[request.json['username']] = request.json['password']
            user[request.json['username']] = request.json['new_password']
            if user in users:
                new_password = user['password']
                return jsonify("Password changed"), 201
            else:
                return jsonify("Input Bad"), 201
        else:
            return jsonify("Please log in"), 201
        #Password is always reset to 'empty'

    #Works
    @app.route('/api/v2/events', methods=['POST', 'GET'])
    def events_json():
        """Add or view events"""
        if request.method == 'POST':
            if 'username' in session:
                location = {}
                location = {request.json['location'], request.json['date']}
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
#        if eventid==events['eventid']:
        if request.method == 'PUT':
            evnts = [event for event in events if event['eventid'] == eventid]
            evnts[0]['eventid'] = {request.json['eventid'],
                                   request.json['location'],
                                   request.json['date']}

            return jsonify({'event':evnts[0]}), 201

        if request.method == 'DELETE':
            evnt = [event for event in events if event['eventid'] == eventid]
            events.remove(evnt[0])
#            return jsonify({"events":events})
#        else:
#            return jsonify("Please edit or delete an existing event")

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
