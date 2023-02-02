import dateutil.parser as dateparser
from scripts import note, parser

def parse_title_for_tag(title, tags):
    for t in tags:
        tag_index = title.lower().find(t.tag_name.lower())
        if tag_index == 0:  # There exists a tag which is a prefix of the title
            return t
    return None # No matching tag found
            
def parse_title_for_date(title):
    try:
        parsed_date = dateparser.parse(title, fuzzy=True, default=None)
        print(parsed_date)
        return parsed_date.ctime()
    except: # Title doesn't contain a date
        return None