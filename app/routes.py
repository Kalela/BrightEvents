#contains RESTful apis
from flask import Flask,jsonify,request,session

from app import app

users =[{'kalela':'Kalela'},{'khal':'khal'},{'user':'password'}]
events=[{'eventid':'Naiconn'},{'eventid':'Safaricom Sevens'},{'eventid':'Python Leaders Summit'}]

class my_apis():
    #Works
    @app.route('/api/v2/auth/register', methods=['POST'])
    def register_page_json():
        user = {}
        user[request.json['username']]=request.json['password']
        users.append(user)
        return jsonify({'users':users})
    #{"username":"user" , "password":"123"} for input
    #Works
    @app.route('/api/v2/auth/login',methods=['POST'])
    def login_json():
        user = {}
        user[request.json['username']]=request.json['password']
        if user in users:
            session['username']=request.json['username']
            return jsonify("Logged in")
        else:
            return jsonify("Please sign up or review your login info")
    #{"username":"user" , "password":"123"} for input
    
    #Works
    @app.route('/api/v2/auth/logout',methods=['POST'])
    def logout_json():
        user = {}
        if 'username' in session:
            session.pop('username')
            return jsonify("User logged out")
        else:
            return jsonify('User is not logged in')
        #{'username':'kalela'}



    @app.route('/api/v2/auth/reset-password',methods=['POST'])
    def reset_password_json():
        if 'username' in session:
            session_name = jsonify(session['username'])
            reset = jsonify('empty')
            user[session_name]=reset['password']
            
            return jsonify(users[session_name])
            


    #Works
    @app.route('/api/v2/events/',methods=['POST'])
    def new_event_json():
        
        event = {'eventid':request.json['eventid']}#put in condition to check bad input. test and see error
        #use session to attach user to their events
        #add event info...location,etc
        events.append(event)
        return jsonify({'events':events},201,)


    #Works, remember double quotes
    @app.route('/api/v2/events/<eventid>',methods=['PUT'])
    def event_update_json(eventid):#check if event exists
        evnts = [event for event in events if event['eventid']==eventid]
        evnts[0]['eventid'] = request.json['eventid']
        
        return jsonify({'event':evnts[0]},201)

    #Works
    @app.route('/api/v2/events/<eventid>',methods=['DELETE'])
    def event_delete_json(eventid):#check if event exists first
        evnt = [event for event in events if event['eventid']==eventid]
        events.remove(evnt[0])
        return jsonify({"events":events})

    #Works. Merge with 'Post' /api/v2/events/
    @app.route('/api/v2/events', methods=['GET'])
    def event_page_json():
        return jsonify ({'events':events},200)

    #Works
    @app.route('/api/v2/events/<eventid>/rsvp', methods=['POST'])
    def rsvp_json(eventid):
        evn = [event for event in events if event['eventid']==eventid]
        evn[0]['eventid'] += ' RSVP Sent'
        return jsonify({"events":events})



    if __name__== '__main__':
        app.run(debug=True)
        
