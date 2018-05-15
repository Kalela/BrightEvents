import datetime
from flask import request
from webapi.helper_functions import pagination, post_event, Category
from webapi.helper_functions import print_events, utc_offset, date_check
from webapi.helper_functions import edit_event

catgory = Category()

def get_events_helper(Event):
    """Help view all events"""
    location = request.args.get('location')
    category = request.args.get('category')
    q = request.args.get('q')
    try:
        limit = int(request.args.get('limit'))
        page = int(request.args.get('page'))
    except:
        limit = 10
        page = 1
    user_input = "get_all"
    if category or location or q:
        user_input = category or location or q
    check_input_dict = {
        category: lambda: Event.filter_category(category, limit, page),
        location: lambda: Event.filter_location(location, limit, page),
        q: lambda: Event.query.filter(Event.eventname.ilike('%{}%'.format(q))).paginate(per_page=limit, page=page),
        "get_all": lambda: Event.get_all_pages(limit, page)
        }
    events_page_object = check_input_dict.get(user_input, "Something went wrong!!")()
    status_code = 200
    result = {"Events": print_events(pagination(events_page_object)[0]),
                 "Current page": pagination(events_page_object)[1],
                 "All pages": pagination(events_page_object)[2]}
    return result, status_code

def create_events_helper(current_user, Event):
    """Help create new events"""
    status_code = 500
    statement = {}
    if not current_user or current_user.logged_in == False:
        result = {"message":"Please Log In to add events"}, 401
    else:
        eventname = request.data['eventname'].strip()
        location = request.data['location'].strip()
        date = request.data['date'].strip()
        if "message" in str(date_check(date)):
            return date_check(date)[0], date_check(date)[1]
        category = request.data['category'].strip()
        if catgory.category_check(category) == "OK":
            pass
        else:
            return {"message":"Please select a viable category",
                    "options": catgory.category_list}, 406
        result = post_event(eventname, location, date, category, current_user, Event)
    return result[0], result[1]

def online_user_events_helper(current_user, user_public_id, Event):
    """Help view owned events"""
    status_code = 500
    statement = {}
    if user_public_id == current_user.public_id:
        events = Event.query.filter_by(owner=current_user.username).all()
        if events:
            status_code = 200
            statement = {"MyEvents":print_events(events)}
        else:
            status_code = 404
            statement = {"message":"You don't have any events"}
    else:
        status_code = 401
        statement = {"message":"You do not have access to this user's events"}
    return statement, status_code

def event_update_delete_helper(current_user, eventname, db, Event):
    """Help edit delete or view a single event"""
    status_code = 500
    statement = {}
    if current_user and current_user.logged_in == True:
        if request.method == 'PUT':
            updated_event_name = request.data['event_name'].strip()
            date = request.data['date'].strip()
            if "message" in str(date_check(date)):
                return date_check(date)[0], date_check(date)[1]
            location = request.data['location'].strip()
            category = request.data['category'].strip()
            if catgory.category_check(category) == "OK":
                event_data = [updated_event_name, date, location, category, db]
                result = edit_event(Event, current_user, eventname, event_data)
                status_code = result[1]
                statement = result[0]
            else:
                status_code = 406
                statement = {"message":"Please select a viable category",
                             "options": catgory.category_list}
        if request.method == 'DELETE':
            event = Event.get_one(eventname, current_user.username)
            if event:
                event.delete()
                events_page_object = Event.get_all_pages(limit=10, page=1)
                status_code = 205
                statement = {"Event(s)": print_events(pagination(events_page_object)[0]),
                            "Current page": pagination(events_page_object)[1],
                            "All pages": pagination(events_page_object)[2]}
            else:
                status_code = 404
                statement = {"message":"Event you are deleting does not exist"}
    else:
        status_code = 401
        statement = {"message":"Please log in to edit or delete events"}
    return statement, status_code

def get_single_event_helper(username, eventname, Event):
    event = Event.get_one(eventname, username)
    if event:
        events = [event]
        status_code = 200
        statement = {"Event":print_events(events)}
    else:
        status_code = 404
        statement = {"message":"Event you are trying to view does not exist",
                     "tip!":"api/v2/events/<username>/<eventname>"}
    return statement, status_code

def rsvps_helper(current_user, eventname, Rsvp, Event):
    """Help send rsvps and view guests"""
    status_code = 500
    statement = {}
    if request.method == 'POST':
        owner = request.data['owner'].strip()
        if not owner:
            status_code = 428
            statement = {"message":"Please insert the owner of the event you want to rsvp"}
        if not current_user or current_user.logged_in == False:
            status_code = 401
            statement = {"message":"Please log in Before sending RSVP"}
        else:
            event = Event.get_one(eventname, owner)
            if event:
                rsvp = Rsvp.query.filter_by(rsvp_sender=current_user.username).all()
                rsvp_event = Rsvp.query.filter_by(event_id=event.id).all()
                if rsvp and rsvp_event:
                    status_code = 409
                    statement = {"message":"RSVP already sent"}
                else:
                    rsvp = Rsvp(event=event, rsvp_sender=current_user.username)
                    rsvp.save()
                    status_code = 201
                    statement = {"message":"RSVP sent"}
            else:
                status_code = 404
                statement = {"message":"Event does not exist"}
    if request.method == 'GET':
        event = Event.get_one(eventname, current_user.username)
        if event:
            guests = Rsvp.query.filter_by(event_id=event.id).all()
            if guests:
                result = []
                for guest in guests:
                    result.append(guest.rsvp_sender)
                status_code = 200
                statement = {"Guests":result}
            else:
                status_code = 200
                statement = {"message":"Event doesn't have guests yet"}
        else:
            status_code = 404
            statement = {"message":"The event was not found"}
    return statement, status_code
