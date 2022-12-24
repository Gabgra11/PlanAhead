from scripts import tag, note

def filter_by_tags(notes_list, tag_names_list):
    result = []
    for n in notes_list:
        for t in tag_names_list:
            if n.tag and n.tag.name == t:
                result.append(n)
    if len(result) == 0:
        result = notes_list
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
