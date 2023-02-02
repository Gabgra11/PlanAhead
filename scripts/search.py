from scripts import tag, note

def filter_by_tags(notes_list, tag_list):
    result = []
    for n in notes_list:
        for t in tag_list:
            if n.tag and n.tag.id == int(t.id):
                result.append(n)
    if len(result) == 0:    # A filter which would exclude every note
        result = notes_list # should not be used.
    return result

def filter_by_text(notes_list, query):
    result = []
    for n in notes_list:
        if query.lower() in n.title.lower():
            result.append(n)
    return result

def find_note_with_title(notes_list, note_title):
    for n in notes_list:
        if n.title == note_title:
            return n
    return None

def find_tag_with_name(tags_list, tag_name):
    for t in tags_list:
        if t.name == tag_name:
            return t
    return None

def find_note_with_id(notes_list, nid):
    for n in notes_list:
        if n.id == nid:
            return n
    return None

def find_tag_with_id(tags_list, tid):
    for t in tags_list:
        if t.id == tid:
            return t
    return None

# Validates that a new tag meets the following criteria:
#   - new tag name is not a duplicate of a distinct, existing tag name
#   - new tag name is not a prefix of a distinct, existing tag name
#   - no existing tag name is a substring of the new tag name
def validate_new_tag_name(tags_list, new_tag):
    new_name = new_tag.tag_name.strip().lower()
    new_id = str(new_tag.id)
    for t in tags_list:
        existing_name = t.tag_name.strip().lower()
        existing_id = str(t.id)
        if existing_id != new_id and \
           (new_name.find(existing_name) == 0 or \
           existing_name.find(new_name) == 0):
            return False
    return True