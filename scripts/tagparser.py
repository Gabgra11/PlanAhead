from scripts import note, tagparser

def parse_title_for_tag(title, tags):
    print(tags)
    for t in tags:
        tag_index = title.lower().find(t.tag_name.lower())
        if tag_index == 0:  # There exists a tag which is a prefix of the title
            return t
    return None # No matching tag found
            