import re

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
    
    