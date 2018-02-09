import re
import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask import request

def print_events(events):
    result = []
    for event in events:
        event_data = {}
        event_data['eventname'] = event.eventname
        event_data['location'] = event.location
        event_data['date'] = event.date
        event_data['category'] = event.category
        event_data['owner'] = event.event_owner.username
        result.append(event_data)
    return result

class Category(object):
    category_list = ["Bridal", "Educational", "Commemorative", "Product Launch", "Social", "VIP"]
    def category_check(self, category):
        if category in self.category_list:
            return "OK"
        else:
            return "BAD"
        
def utc_offset(string):
    return string[-5:]

def special_characters(string):
    if re.findall('[^A-Za-z0-9]',string):
        return True
    
def check_registration_input(username, email, password):
    message = {}
    if not email:
        message = {"message":"Please insert a valid email"}
    if "@" not in str(email) or ".com" not in str(email):
        message = {"message":"Please insert a valid email"}
    if not username:
        message = {"message":"Please insert username"}
    if not password:
        message = {"message":"Please insert password"}
    return message

def check_password_reset(new_password, confirm_password, user, status_code):
    message = {}
    if not new_password or not confirm_password:
        message = {"message":"Please insert required fields"}
        status_code = 400
    if check_password_hash(user.password, new_password):
        message = {"message":"Password already set"}
        status_code = 409
    if new_password == confirm_password:
        new_password = generate_password_hash(request.form['new_password'], method='sha256')
    else:
        message = {"message":"Passwords don't match"}
        status_code = 409
    return message, status_code, new_password
