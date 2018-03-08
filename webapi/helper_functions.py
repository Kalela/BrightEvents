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
    """Pick values of the current run environment UTC offset"""
    return string[-5:]

def date_check(date):
    """Check correct date input"""
    try:
        date_object = datetime.datetime.strptime(str(date), '%Y/%m/%d')
        return date_object
    except ValueError:
        return {"message":"Wrong date format input(Correct:yy/mm/dd)"}, 400
    
def check_registration_input(username, email, password):
    """Check email input"""
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
    """Check correct inputs for a password reset"""
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

def pagination(events_page_object):
    """Handle outputting pages of data"""
    events = events_page_object.items
    current_page = events_page_object.page
    all_pages = events_page_object.pages
    return events, current_page, all_pages

def post_event(eventname, location, date, category, current_user, Event):
    """Handle posting an event to the database"""
    if eventname and location and date and category:
        event = Event.get_one(eventname, current_user.username)
        try:
            event_date = datetime.datetime.strptime(str(event.date),
                                                    '%Y-%m-%d %H:%M:%S+' + utc_offset(str(event.date)))
        except:
            pass   
        if event and event.location == location and event_date == date_check(date):
            status_code = 409
            statement = {"message":"Event already exists"}
        else:
            event = Event(event_owner=current_user, eventname=eventname,
                          location=location, date=date, category=category)
            events = [event]
            event.save()
            status_code = 201
            statement = {"New event":print_events(events)}
    else:
        status_code = 400
        statement = {"message":"Please insert all required fields!"}
    return statement, status_code
    
