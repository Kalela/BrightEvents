import datetime
from flask import request
from webapi.helper_functions import print_events, utc_offset, Category

catgory = Category()

def get_events_helper(Event):
    try:
        location = request.args.get('location')
        category = request.args.get('category')
        q = request.args.get('q')
        limit = request.args.get('limit')
        if limit:
            limit = int(limit)
        _next = request.args.get('next')
        prev = request.args.get('prev')
        if category:
            events = Event.filter_category(category)
        if location:
            events = Event.filter_location(location)
        if q:
            events = Event.query.filter(Event.eventname.ilike('%{}%'.format(q))).all()
        if not category and not location and not q:
            if not limit:
                limit = 10
            event_pages = Event.get_all_pages(limit, 1)
            events = event_pages.items
            if _next == "y" and event_pages.has_next:
                event_page = Event.get_all_pages(limit, event_pages.next_num)
                events = event_page.items
            if prev == "y" and event_pages.has_prev:
                event_page = Event.get_all_pages(limit, event_pages.prev_num)
                events = event_page.items
        status_code = 200
        statement = {"Events": print_events(events)}
    except Exception as e:
        status_code = 500
        statement = {"Error":str(e)}
    return statement, status_code

def create_events_helper(current_user, Event):
    status_code = 500
    statement = {}
    try:
        user = current_user
        if request.method == 'POST':
            if not user or user.logged_in == False:
                status_code = 401
                statement = {"message":"Please Log In to add events"}
            else:
                eventname = request.form['eventname'].strip()
                location = request.form['location'].strip()
                date = request.form['date'].strip()
                owner = user.username
                try:
                    date_object = datetime.datetime.strptime(str(date), '%Y/%m/%d')
                except ValueError:
                    return {"message":"Wrong date format input(Correct:yy/mm/dd)"}, 400
                category = request.form['category'].strip()
                if catgory.category_check(category) == "OK":
                    pass
                else:
                    return {"message":"Please select a viable category",
                            "options": catgory.category_list}, 406

                if eventname and location and date and category:
                    event = Event.get_one(eventname, owner)
                    if event and event.location == location:
                        event_date = datetime.datetime.strptime(str(event.date),
                                                                '%Y-%m-%d %H:%M:%S+' + utc_offset(str(event.date)))
                        if event_date == date_object:
                            status_code = 409
                            statement = {"message":"Event already exists"}
                        else:
                            event = Event(event_owner=current_user,
                                          eventname=eventname,
                                          location=location, date=date,
                                          category=category)
                            event.save()
                            status_code = 201
                            statement = {"message":"Event has been created",
                                         "caution!":"Event with same name and location exists"}


                    else:
                        event = Event(event_owner=current_user,
                                      eventname=eventname,
                                      location=location,
                                      date=date, category=category)
                        events = [event]
                        event.save()
                        status_code = 201
                        statement = {"New event":print_events(events)}
                else:
                    status_code = 400
                    statement = {"message":"Please insert valid event"}

    except Exception as e:
        status_code = 500
        statement = {"Error":str(e)}
    return statement, status_code

def online_user_events_helper(current_user, Event):
    status_code = 500
    statement = {}
    try:
        events = Event.query.filter_by(owner=current_user.username).all()
        if events:
            status_code = 200
            statement = {"My Events":print_events(events)}
        else:
            status_code = 404
            statement = {"message":"You don't have any events"}
    except Exception as e:
        status_code = 500
        statement = {"Error":str(e)}
    return statement, status_code

def event_update_delete_helper(current_user, eventname, db, Event):
    status_code = 500
    statement = {}
    try:
        user = current_user
        if user and user.logged_in == True:
            if request.method == 'PUT':
                updated_event_name = request.form['event_name'].strip()
                date = request.form['date'].strip()
                try:
                    date_object = datetime.datetime.strptime(str(date), '%Y/%m/%d')
                except ValueError:
                    return {"message":"Wrong date format input(Correct:yy/mm/dd)"}, 400
                location = request.form['location'].strip()
                category = request.form['category'].strip()
                if catgory.category_check(category) == "OK":
                    pass
                else:
                    status_code = 406
                    statement = {{"message":"Please select a viable category"},
                                 {"options": catgory.category_list}}
                event = Event.get_one(eventname, user.username)
                if event is True:
                    event.eventname = updated_event_name
                    event.location = location
                    event.date = date
                    event.category = category
                    db.session.commit()
                    status_code = 202
                    statement = {"Event updated to:":{
                        "eventname":updated_event_name,
                        "location":location,
                        "date":date,
                        "category":category
                    }}
                else:
                    status_code = 404
                    statement = {"message":"Event you are editing does not exist"}

            if request.method == 'DELETE':
                event = Event.get_one(eventname, user.username)
                if event:
                    event.delete()
                    event_pages = Event.get_all_pages(limit=10, page=1)
                    events = event_pages.items
                    status_code = 205
                    statement = {"Event(s)": print_events(events)}
                else:
                    status_code = 404
                    statement = {"message":"Event you are deleting does not exist"}

            if request.method == 'GET':
                owner = request.args.get('owner')
                if not owner:
                    owner = user.username
                event = Event.get_one(eventname, owner.strip())
                if event:
                    events = [event]
                    status_code = 200
                    statement = {"Event":print_events(events)}
                else:
                    status_code = 404
                    statement = {"message":"Event you are trying to view does not exist",
                                 "tip!":"Insert event owner as parameter"}  
        else:
            status_code = 401
            statement = {"message":"Please log in to edit or delete events"}
    except Exception as e:
        status_code = 500
        statement = {"Error":str(e)}
    return statement, status_code

def rsvps_helper(current_user, eventname, Rsvp, Event):
    status_code = 500
    statement = {}
    try:
        if request.method == 'POST':
            owner = request.form['owner'].strip()
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
                        rsvp = Rsvp(event=event, rsvp_sender=user.username)
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

    except Exception as e:
        status_code = 500
        statement = {"Error":str(e)}
    return statement, status_code
