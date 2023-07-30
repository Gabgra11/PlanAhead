import dateutil.parser as dateparser
from scripts import note, parser

"""
Returns (tag, new_title)
tag: existing tag found as a prefix in title
new_title: title without tag prefix
"""
def parse_title_for_tag(title, tags):
    for t in tags:
        tag_index = title.lower().find(t.tag_name.lower())
        if tag_index == 0:  # There exists a tag which is a prefix of the title
            new_title = title[len(t.tag_name):].strip() # Slice off length of tag prefix.
            return (t, new_title)
    return (None, title) # No matching tag found
   
"""
Returns (date, new_title)
date: existing date found after delimiter
new_title: title without date or delimiter
"""
def parse_title_for_date(title, delimiter=""):
    delimiter_index = title.find(delimiter)
    if (delimiter_index >= 0):
        date_string = title[delimiter_index:]
    try:
        parsed_date = dateparser.parse(date_string, fuzzy=True, default=None)
        new_title = title[:delimiter_index].strip()
        return (parsed_date.strftime("%Y-%m-%dT%H:%M"), new_title)
        #return (parsed_date.ctime(), new_title)
    except: # Title doesn't contain a date
        return (None, title)