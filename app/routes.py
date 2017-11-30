#contains RESTful apis
from flask import Flask,jsonify,request

from app import app

users =[]
events=[{'eventid':'Naiconn'},{'eventid':'Safaricom Sevens'},{'eventid':'Python Leaders Summit'}]



@app.route('/api/v2/auth/register', methods=['POST'])
def register_page_json():

    username=request.json['username'],
    password=request.json['password'] 

    users.append({username:username,password:password})
    return jsonify({"users":users},201)


@app.route('/api/v2/auth/login',methods=['POST'])
def login_json():
    username = {'name':request.json['name']}
    password = {'password':request.json['password']}
    for user in users:
        if user['username']==username and user['password'] ==password:
            return jsonify('logged in')
    

@app.route('/api/v2/auth/logout',methods=['POST'])
def logout_json():
    pass



@app.route('/api/v2/auth/reset-password',methods=['POST'])
def reset_password_json():
    username = {'name':request.json['name']}
    new_password = {'password':request.json['password']}
    for user in users:
        if user['username']==username and user['password']==password:
                user['password']=new_password
                return jsonify('password changed to',new_password)



@app.route('/api/v2/events/',methods=['POST'])
def new_event_json():
    event = {'eventid':request.json['eventid']}
    
    events.append(event)
    return jsonify({'users':users},200)
     
    

@app.route('/api/v2/events/<eventid>',methods=['PUT'])
def event_put_json(eventid):
    evnts = [events for events in events if event['eventid']==name]
    evnts[0]['name'] = request.json['name']
    return jsonify({'event':evnts[0]})


@app.route('/api/v2/events/<eventid>',methods=['DELETE'])
def event_delete_json(eventid):
    evnt = [event for event in events if event['eventid']==eventid]
    events.remove(evnt[0])
    return jsonify({"events":events})
    

@app.route('/api/v2/events', methods=['GET'])
def event_page_json():
    return jsonify ({'events':events},200)
 

@app.route('/api/v2/events/<eventid>/rsvp', methods=['POST'])
def rsvp_json():
    pass



if __name__== '__main__':
    app.run(debug=True)
        
