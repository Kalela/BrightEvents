#contains RESTful apis
from flask import Flask, jsonify, request, session
from app import app


users = [{'kalela':'Kalela'}, {'khal':'khal'}, {'user':'password'}]
events = []
user_events = []

class MyApis(object):
    #Works
    @app.route('/api/v2/auth/register', methods=['POST'])
    def register_page_json():
        user = {}
        user[request.json['username']] = request.json['password']
        users.append(user)
        return jsonify({'users':users}), 201
    #{"username":"user" , "password":"123"} for input
    #Works
    @app.route('/api/v2/auth/login', methods=['POST'])
    def login_json():
        user = {}
        user[request.json['username']] = request.json['password']
        if user in users:
            session['username'] = request.json['username']
            return jsonify("Logged in"), 201
        else:
            return jsonify("Please sign up or review your login info")
    #{"username":"user" , "password":"123"} for input

    #Works
    @app.route('/api/v2/auth/logout', methods=['POST'])
    def logout_json():
        user = {}
        if 'username' in session:
            session.pop('username')
            return jsonify("User logged out"), 201
        else:
            return jsonify('User is not logged in')
        #{'username':'kalela'}


    #Works  ??
    @app.route('/api/v2/auth/reset-password', methods=['POST'])
    def reset_password_json():
        if 'username' in session:
            user = {}
            user[request.json['username']] = request.json['password']
            user[request.json['username']] = request.json['new_password']
            if user in users:
                new_password = user['password']
                return jsonify("Password changed"), 201
            else:
                return jsonify("Input Bad")
        else:
            return jsonify("Please log in")
        #Password is always reset to 'empty'

    #Works
    @app.route('/api/v2/events/', methods=['POST', 'GET'])
    def events_json():
        if request.method == 'POST':
            if 'username' in session:
                location = {}
                location = {request.json['location'], request.json['date']}
                event = {}
                event[request.json['eventid']] = str(location)

                if event in events:
                    return jsonify("Event is already added")
                else:
                    events.append(event)
                    user_events.append(event)
                    return jsonify({'events':events}, {"user events":user_events}), 201
            else:
                return jsonify("Please Log In to add events")
        if request.method == 'GET':
            return jsonify({'events':events}), 200

    #Fails
    @app.route('/api/v2/events/<eventid>', methods=['PUT', 'DELETE'])
    def event_update_json(eventid):#check if event exists
#        if eventid==events['eventid']:
            if request.method == 'PUT':
                evnts = [event for event in events if event['eventid']==eventid]
                evnts[0]['eventid'] = request.json['eventid'], request.json['location'],request.json['date']

                return jsonify({'event':evnts[0]}),201
               
            if request.method=='DELETE':
                        evnt = [event for event in events if event['eventid']==eventid]
            events.remove(evnt[0])
#            return jsonify({"events":events})
         
#        else:
#            return jsonify("Please edit or delete an existing event")
  
 

    #Fails
    @app.route('/api/v2/events/<eventid>/rsvp', methods=['POST'])
    def rsvp_json(eventid):
        evn = [event for event in events if event['eventid']==eventid]
        evn[0]['eventid'] += ' RSVP Sent'
        return jsonify({"events":events})



    if __name__== '__main__':
        app.run(debug=True)
        
